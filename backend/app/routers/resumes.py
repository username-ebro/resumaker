"""
Resumes Router
API endpoints for resume generation, editing, and management
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from ..services.resume_generator import ResumeGenerator
from ..services.fact_checker import FactChecker
from ..services.ats_optimizer import ATSOptimizer
from ..services.pdf_exporter import PDFExporter
from ..services.docx_exporter import DOCXExporter
from ..database import get_supabase
from datetime import datetime

router = APIRouter(prefix="/resumes", tags=["resumes"])

# Pydantic models
class GenerateResumeRequest(BaseModel):
    job_description: Optional[str] = None
    target_role: Optional[str] = None
    job_posting_id: Optional[str] = None

class GenerateGenericResumeRequest(BaseModel):
    prompt: str

class UpdateResumeRequest(BaseModel):
    resume_structure: Dict[str, Any]

class ResolveFlagRequest(BaseModel):
    resolution_notes: str

# Initialize services
resume_gen = ResumeGenerator()
fact_checker = FactChecker()
ats_optimizer = ATSOptimizer()
pdf_exporter = PDFExporter()
docx_exporter = DOCXExporter()
supabase = get_supabase()


@router.post("/generate")
async def generate_resume(
    request: GenerateResumeRequest,
    user_id: str  # In production, get from auth token
):
    """
    Generate a new resume from knowledge base

    If job_posting_id provided, pulls job description from database
    Otherwise uses provided job_description or generates generic resume
    """
    try:
        job_description = request.job_description
        target_role = request.target_role

        # If job posting ID provided, fetch from database
        if request.job_posting_id:
            job_result = supabase.table("job_postings")\
                .select("*")\
                .eq("id", request.job_posting_id)\
                .single()\
                .execute()

            job_data = job_result.data
            job_description = job_data['job_description']
            target_role = job_data['job_title']

        # Generate resume structure
        resume_structure = await resume_gen.generate_resume(
            user_id=user_id,
            job_description=job_description,
            target_role=target_role
        )

        # Apply ATS optimization
        optimized_resume = ats_optimizer.optimize_resume(resume_structure)

        # Generate HTML version
        html_resume = await resume_gen.generate_html_resume(optimized_resume)

        # Create resume version in database
        resume_record = {
            "user_id": user_id,
            "job_posting_id": request.job_posting_id,
            "content": optimized_resume,
            "html_content": html_resume,
            "status": "draft",
            "version_number": await _get_next_version_number(user_id)
        }

        result = supabase.table("resume_versions").insert(resume_record).execute()
        resume_version_id = result.data[0]['id']

        # Run fact verification
        verification_result = await fact_checker.verify_resume(
            user_id=user_id,
            resume_structure=optimized_resume,
            resume_version_id=resume_version_id
        )

        # Update resume status based on verification
        new_status = "fact_check_complete" if not verification_result['requires_review'] else "fact_check_pending"

        supabase.table("resume_versions")\
            .update({"status": new_status})\
            .eq("id", resume_version_id)\
            .execute()

        return {
            "success": True,
            "resume_version_id": resume_version_id,
            "resume": optimized_resume,
            "html": html_resume,
            "verification": verification_result,
            "ats_score": optimized_resume['optimization_report']['ats_score']
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-generic")
async def generate_generic_resume(
    request: GenerateGenericResumeRequest,
    user_id: str
):
    """
    Generate a generic resume based on freeform prompt

    Uses confirmed knowledge entities to select relevant facts based on the prompt.
    Example prompt: "applying for concession stand role"

    Args:
        request.prompt: Freeform text describing what to emphasize
        user_id: User ID

    Returns:
        Generated resume with selected facts
    """
    try:
        print(f"Generating generic resume for prompt: {request.prompt}")

        # 1. Fetch all confirmed knowledge entities for user
        result = supabase.table("knowledge_entities")\
            .select("*")\
            .eq("user_id", user_id)\
            .eq("is_confirmed", True)\
            .execute()

        confirmed_entities = result.data
        print(f"Found {len(confirmed_entities)} confirmed knowledge entities")

        if not confirmed_entities:
            raise HTTPException(
                status_code=400,
                detail="No confirmed knowledge entities found. Please confirm some facts first."
            )

        # 2. Use Claude to select relevant entities based on prompt
        entities_text = "\n\n".join([
            f"ID: {i}\nType: {e['entity_type']}\nTitle: {e['title']}\nDescription: {e['description']}"
            for i, e in enumerate(confirmed_entities)
        ])

        selection_prompt = f"""You are helping generate a resume. The user wants to emphasize: "{request.prompt}"

Here are all their confirmed knowledge entities:

{entities_text}

Which entities are most relevant for this goal? Return a JSON array of entity IDs (the numbers) that should be included, prioritized by relevance.

Example format: {{"selected_ids": [0, 3, 5, 7]}}

Focus on:
1. Direct experience related to the prompt
2. Transferable skills
3. Relevant accomplishments
4. Related education/certifications

Return ONLY the JSON, nothing else."""

        message = resume_gen.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{"role": "user", "content": selection_prompt}]
        )

        # Parse selection response
        import json
        selection_text = message.content[0].text.strip()
        # Extract JSON if wrapped in markdown
        if '```' in selection_text:
            selection_text = selection_text.split('```')[1].replace('json', '').strip()

        selected_data = json.loads(selection_text)
        selected_ids = selected_data.get('selected_ids', [])
        print(f"Selected {len(selected_ids)} relevant entities")

        # 3. Build filtered knowledge base
        selected_entities = [confirmed_entities[i] for i in selected_ids if i < len(confirmed_entities)]

        # Convert to knowledge base format expected by resume generator
        knowledge_base = []
        for entity in selected_entities:
            kb_entry = {
                'id': entity['id'],
                'user_id': entity['user_id'],
                'title': entity['title'],
                'content': entity.get('structured_data', {}) or {'description': entity['description']},
                'knowledge_type': _map_entity_type_to_knowledge_type(entity['entity_type']),  # FIXED: removed 'self.'
                'tags': [],
                'date_range': None,
                'created_at': entity['created_at']
            }

            # Set date range if available
            if entity.get('start_date') or entity.get('end_date'):
                start = entity.get('start_date', '1900-01-01')
                end = entity.get('end_date', '9999-12-31')
                kb_entry['date_range'] = f"[{start},{end})"

            knowledge_base.append(kb_entry)

        print(f"Converted to {len(knowledge_base)} knowledge base entries")

        # 4. Get user profile
        profile = await resume_gen._fetch_user_profile(user_id)

        # 5. Organize knowledge
        organized = resume_gen._organize_knowledge(knowledge_base)

        # 6. Generate resume with context from prompt
        summary = await resume_gen._generate_summary(
            profile=profile,
            knowledge=organized,
            target_role=request.prompt,  # Use prompt as target role context
            keywords=[]
        )

        experience = await resume_gen._generate_experience(
            knowledge=organized,
            keywords=[]
        )

        skills = await resume_gen._generate_skills(
            knowledge=organized,
            keywords=[]
        )

        education = resume_gen._generate_education(organized)
        certifications = resume_gen._generate_certifications(organized)

        # 7. Assemble resume
        resume_structure = {
            "contact_info": {
                "name": profile.get("full_name", ""),
                "email": profile.get("email", ""),
                "phone": profile.get("phone", ""),
                "location": profile.get("location", ""),
                "linkedin": profile.get("linkedin_url", ""),
                "portfolio": profile.get("portfolio_url", "")
            },
            "summary": summary,
            "experience": experience,
            "skills": skills,
            "education": education,
            "certifications": certifications,
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "knowledge_base_entries_used": len(knowledge_base),
                "target_context": request.prompt,
                "job_targeted": False,
                "generation_type": "generic"
            }
        }

        # 8. Apply ATS optimization
        optimized = ats_optimizer.optimize_resume(resume_structure)

        # 9. Generate HTML
        html = await resume_gen.generate_html_resume(optimized)

        # 10. Save to database
        resume_record = {
            "user_id": user_id,
            "job_posting_id": None,
            "content": optimized,
            "html_content": html,
            "status": "draft",
            "version_number": await _get_next_version_number(user_id)
        }

        result = supabase.table("resume_versions").insert(resume_record).execute()
        resume_id = result.data[0]['id']

        print(f"Generated resume {resume_id}")

        return {
            "success": True,
            "resume_id": resume_id,
            "resume": optimized,
            "html": html,
            "entities_used": len(selected_entities),
            "prompt": request.prompt
        }

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse AI response: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume generation failed: {str(e)}")


def _map_entity_type_to_knowledge_type(entity_type: str) -> str:
    """Map knowledge_entities.entity_type to user_knowledge_base.knowledge_type"""
    mapping = {
        'work_experience': 'experience',
        'job_experience': 'experience',
        'education': 'education',
        'skill': 'skill',
        'achievement': 'accomplishment',
        'accomplishment': 'accomplishment',
        'certification': 'certification',
        'project': 'project',
        'metric': 'metric',
        'story': 'story'
    }
    return mapping.get(entity_type.lower(), 'experience')


@router.get("/list")
async def list_resumes(user_id: str):
    """Get all resume versions for user"""
    try:
        result = supabase.table("resume_versions")\
            .select("id, created_at, status, version_number, job_posting_id, content")\
            .eq("user_id", user_id)\
            .order("created_at", desc=True)\
            .execute()

        resumes = []
        for resume in result.data:
            # Get job info if linked
            job_title = None
            company = None
            if resume['job_posting_id']:
                job_result = supabase.table("job_postings")\
                    .select("job_title, company_name")\
                    .eq("id", resume['job_posting_id'])\
                    .single()\
                    .execute()
                job_title = job_result.data['job_title']
                company = job_result.data['company_name']

            resumes.append({
                "id": resume['id'],
                "version": resume['version_number'],
                "status": resume['status'],
                "created_at": resume['created_at'],
                "job_title": job_title,
                "company": company,
                "ats_score": resume['content'].get('optimization_report', {}).get('ats_score', 0)
            })

        return {"resumes": resumes}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{resume_id}")
async def get_resume(resume_id: str, user_id: str):
    """Get full resume by ID"""
    try:
        result = supabase.table("resume_versions")\
            .select("*")\
            .eq("id", resume_id)\
            .eq("user_id", user_id)\
            .single()\
            .execute()

        resume = result.data

        # Get fact check flags
        flags = await fact_checker.get_flags_for_resume(resume_id)

        return {
            "resume": resume,
            "flags": flags
        }

    except Exception as e:
        raise HTTPException(status_code=404, detail="Resume not found")


@router.put("/{resume_id}")
async def update_resume(
    resume_id: str,
    request: UpdateResumeRequest,
    user_id: str
):
    """Update resume structure"""
    try:
        # Re-optimize after edits
        optimized = ats_optimizer.optimize_resume(request.resume_structure)

        # Regenerate HTML
        html = await resume_gen.generate_html_resume(optimized)

        # Update in database
        supabase.table("resume_versions")\
            .update({
                "content": optimized,
                "html_content": html,
                "updated_at": datetime.utcnow().isoformat()
            })\
            .eq("id", resume_id)\
            .eq("user_id", user_id)\
            .execute()

        return {
            "success": True,
            "resume": optimized,
            "html": html
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{resume_id}/verify")
async def reverify_resume(resume_id: str, user_id: str):
    """Re-run fact verification on resume"""
    try:
        # Get resume
        result = supabase.table("resume_versions")\
            .select("content")\
            .eq("id", resume_id)\
            .eq("user_id", user_id)\
            .single()\
            .execute()

        resume_structure = result.data['content']

        # Run verification
        verification_result = await fact_checker.verify_resume(
            user_id=user_id,
            resume_structure=resume_structure,
            resume_version_id=resume_id
        )

        # Update status
        new_status = "fact_check_complete" if not verification_result['requires_review'] else "fact_check_pending"

        supabase.table("resume_versions")\
            .update({"status": new_status})\
            .eq("id", resume_id)\
            .execute()

        return {
            "success": True,
            "verification": verification_result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{resume_id}/flags")
async def get_resume_flags(resume_id: str, user_id: str):
    """Get all fact check flags for resume"""
    try:
        # Verify user owns this resume
        result = supabase.table("resume_versions")\
            .select("id")\
            .eq("id", resume_id)\
            .eq("user_id", user_id)\
            .execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Resume not found")

        flags = await fact_checker.get_flags_for_resume(resume_id)

        return {"flags": flags}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flags/{flag_id}/resolve")
async def resolve_flag(
    flag_id: str,
    request: ResolveFlagRequest,
    user_id: str
):
    """Mark a fact check flag as resolved"""
    try:
        success = await fact_checker.resolve_flag(
            flag_id=flag_id,
            resolution=request.resolution_notes,
            resolved_by=user_id
        )

        if success:
            return {"success": True}
        else:
            raise HTTPException(status_code=500, detail="Failed to resolve flag")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{resume_id}/finalize")
async def finalize_resume(resume_id: str, user_id: str):
    """Mark resume as finalized (ready for export)"""
    try:
        # Check if any unresolved high/medium severity flags
        flags = await fact_checker.get_flags_for_resume(resume_id)
        unresolved_critical = [
            f for f in flags
            if not f.get('resolved', False) and f['severity'] in ['high', 'medium']
        ]

        if unresolved_critical:
            return {
                "success": False,
                "error": "Cannot finalize resume with unresolved critical flags",
                "unresolved_count": len(unresolved_critical)
            }

        # Update status
        supabase.table("resume_versions")\
            .update({"status": "finalized"})\
            .eq("id", resume_id)\
            .eq("user_id", user_id)\
            .execute()

        return {"success": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{resume_id}/export/html")
async def export_html(resume_id: str, user_id: str):
    """Export resume as HTML"""
    try:
        result = supabase.table("resume_versions")\
            .select("html_content")\
            .eq("id", resume_id)\
            .eq("user_id", user_id)\
            .single()\
            .execute()

        return {
            "html": result.data['html_content']
        }

    except Exception as e:
        raise HTTPException(status_code=404, detail="Resume not found")


@router.get("/stats/verification")
async def get_verification_stats(user_id: str):
    """Get overall verification statistics for user"""
    try:
        stats = await fact_checker.get_verification_summary(user_id)
        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{resume_id}/export/pdf")
async def export_pdf(resume_id: str, user_id: str):
    """Export resume as PDF"""
    try:
        # Get resume HTML
        result = supabase.table("resume_versions")\
            .select("html_content, content")\
            .eq("id", resume_id)\
            .eq("user_id", user_id)\
            .single()\
            .execute()

        html_content = result.data['html_content']

        # Convert to PDF
        pdf_stream = pdf_exporter.get_pdf_stream(html_content)

        # Get contact name for filename
        contact_info = result.data['content'].get('contact_info', {})
        name = contact_info.get('name', 'Resume').replace(' ', '_')

        return StreamingResponse(
            pdf_stream,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={name}_Resume.pdf"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=404, detail="Resume not found")


@router.get("/{resume_id}/export/docx")
async def export_docx(resume_id: str, user_id: str):
    """Export resume as DOCX"""
    try:
        # Get resume structure
        result = supabase.table("resume_versions")\
            .select("content")\
            .eq("id", resume_id)\
            .eq("user_id", user_id)\
            .single()\
            .execute()

        resume_structure = result.data['content']

        # Convert to DOCX
        docx_stream = docx_exporter.get_docx_stream(resume_structure)

        # Get contact name for filename
        contact_info = resume_structure.get('contact_info', {})
        name = contact_info.get('name', 'Resume').replace(' ', '_')

        return StreamingResponse(
            docx_stream,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f"attachment; filename={name}_Resume.docx"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=404, detail="Resume not found")


@router.post("/{resume_id}/star")
async def toggle_star(resume_id: str, request: dict):
    """Toggle star status for a resume"""
    try:
        is_starred = request.get("is_starred", False)

        result = supabase.table("resume_versions")\
            .update({"is_starred": is_starred, "updated_at": datetime.utcnow().isoformat()})\
            .eq("id", resume_id)\
            .execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Resume not found")

        return {"success": True, "is_starred": is_starred}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update star status: {str(e)}")


@router.post("/{resume_id}/archive")
async def toggle_archive(resume_id: str, request: dict):
    """Toggle archive status for a resume"""
    try:
        is_archived = request.get("is_archived", False)

        result = supabase.table("resume_versions")\
            .update({"is_archived": is_archived, "updated_at": datetime.utcnow().isoformat()})\
            .eq("id", resume_id)\
            .execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Resume not found")

        return {"success": True, "is_archived": is_archived}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update archive status: {str(e)}")


@router.delete("/{resume_id}")
async def delete_resume(resume_id: str):
    """Delete a resume permanently"""
    try:
        # First, delete associated fact check flags
        supabase.table("fact_check_flags").delete().eq("resume_version_id", resume_id).execute()

        # Then delete the resume
        result = supabase.table("resume_versions")\
            .delete()\
            .eq("id", resume_id)\
            .execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Resume not found")

        return {"success": True, "message": "Resume deleted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete resume: {str(e)}")


async def _get_next_version_number(user_id: str) -> int:
    """Get next version number for user's resumes"""
    result = supabase.table("resume_versions")\
        .select("version_number")\
        .eq("user_id", user_id)\
        .order("version_number", desc=True)\
        .limit(1)\
        .execute()

    if result.data:
        return result.data[0]['version_number'] + 1
    else:
        return 1
