"""
Resumes Router
API endpoints for resume generation, editing, and management
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from ..services.resume_generator import ResumeGenerator
from ..services.truth_checker import TruthChecker
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

class UpdateResumeRequest(BaseModel):
    resume_structure: Dict[str, Any]

class ResolveFlagRequest(BaseModel):
    resolution_notes: str

# Initialize services
resume_gen = ResumeGenerator()
truth_checker = TruthChecker()
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
            job_description = job_data['description_text']
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
            "resume_structure": optimized_resume,
            "html_content": html_resume,
            "status": "draft",
            "version_number": await _get_next_version_number(user_id)
        }

        result = supabase.table("resume_versions").insert(resume_record).execute()
        resume_version_id = result.data[0]['id']

        # Run truth verification
        verification_result = await truth_checker.verify_resume(
            user_id=user_id,
            resume_structure=optimized_resume,
            resume_version_id=resume_version_id
        )

        # Update resume status based on verification
        new_status = "truth_check_complete" if not verification_result['requires_review'] else "truth_check_pending"

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


@router.get("/list")
async def list_resumes(user_id: str):
    """Get all resume versions for user"""
    try:
        result = supabase.table("resume_versions")\
            .select("id, created_at, status, version_number, job_posting_id, resume_structure")\
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
                "ats_score": resume['resume_structure'].get('optimization_report', {}).get('ats_score', 0)
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

        # Get truth check flags
        flags = await truth_checker.get_flags_for_resume(resume_id)

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
                "resume_structure": optimized,
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
    """Re-run truth verification on resume"""
    try:
        # Get resume
        result = supabase.table("resume_versions")\
            .select("resume_structure")\
            .eq("id", resume_id)\
            .eq("user_id", user_id)\
            .single()\
            .execute()

        resume_structure = result.data['resume_structure']

        # Run verification
        verification_result = await truth_checker.verify_resume(
            user_id=user_id,
            resume_structure=resume_structure,
            resume_version_id=resume_id
        )

        # Update status
        new_status = "truth_check_complete" if not verification_result['requires_review'] else "truth_check_pending"

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
    """Get all truth check flags for resume"""
    try:
        # Verify user owns this resume
        result = supabase.table("resume_versions")\
            .select("id")\
            .eq("id", resume_id)\
            .eq("user_id", user_id)\
            .execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Resume not found")

        flags = await truth_checker.get_flags_for_resume(resume_id)

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
    """Mark a truth check flag as resolved"""
    try:
        success = await truth_checker.resolve_flag(
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
        flags = await truth_checker.get_flags_for_resume(resume_id)
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
        stats = await truth_checker.get_verification_summary(user_id)
        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{resume_id}/export/pdf")
async def export_pdf(resume_id: str, user_id: str):
    """Export resume as PDF"""
    try:
        # Get resume HTML
        result = supabase.table("resume_versions")\
            .select("html_content, resume_structure")\
            .eq("id", resume_id)\
            .eq("user_id", user_id)\
            .single()\
            .execute()

        html_content = result.data['html_content']

        # Convert to PDF
        pdf_stream = pdf_exporter.get_pdf_stream(html_content)

        # Get contact name for filename
        contact_info = result.data['resume_structure'].get('contact_info', {})
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
            .select("resume_structure")\
            .eq("id", resume_id)\
            .eq("user_id", user_id)\
            .single()\
            .execute()

        resume_structure = result.data['resume_structure']

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
