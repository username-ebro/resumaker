"""
Jobs Router
API endpoints for job posting management and keyword analysis
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from ..services.job_matcher import JobMatcher
from ..services.ats_optimizer import ATSOptimizer
from ..database import get_supabase

router = APIRouter(prefix="/jobs", tags=["jobs"])

# Pydantic models
class AddJobRequest(BaseModel):
    job_description: str
    job_url: Optional[str] = None
    company_name: Optional[str] = None

class AnalyzeMatchRequest(BaseModel):
    job_id: str
    resume_id: str

# Initialize services
job_matcher = JobMatcher()
ats_optimizer = ATSOptimizer()
supabase = get_supabase()


@router.post("/add")
async def add_job_posting(
    request: AddJobRequest,
    user_id: str  # In production, get from auth token
):
    """
    Add and parse a new job posting

    Extracts keywords, requirements, and detects ATS system
    """
    try:
        # Parse job description
        job_data = await job_matcher.parse_job_description(
            job_description=request.job_description,
            job_url=request.job_url,
            company_name=request.company_name
        )

        # Store in database
        job_id = await job_matcher.store_job_posting(
            user_id=user_id,
            job_data=job_data,
            job_description_full=request.job_description
        )

        return {
            "success": True,
            "job_id": job_id,
            "job_data": job_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_job_postings(user_id: str):
    """Get all job postings for user"""
    try:
        jobs = await job_matcher.get_user_job_postings(user_id)

        return {"jobs": jobs}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{job_id}")
async def get_job_posting(job_id: str, user_id: str):
    """Get full job posting details"""
    try:
        result = supabase.table("job_postings")\
            .select("*")\
            .eq("id", job_id)\
            .eq("user_id", user_id)\
            .single()\
            .execute()

        job = result.data

        # Get ATS system info if available
        if job.get('ats_system_id'):
            ats_result = supabase.table("ats_systems")\
                .select("*")\
                .eq("id", job['ats_system_id'])\
                .single()\
                .execute()
            job['ats_system_details'] = ats_result.data

        return {"job": job}

    except Exception as e:
        raise HTTPException(status_code=404, detail="Job posting not found")


@router.post("/analyze-match")
async def analyze_job_match(
    request: AnalyzeMatchRequest,
    user_id: str
):
    """
    Analyze how well a resume matches a job posting

    Returns match score, missing keywords, and recommendations
    """
    try:
        # Get job posting
        job_result = supabase.table("job_postings")\
            .select("*")\
            .eq("id", request.job_id)\
            .eq("user_id", user_id)\
            .single()\
            .execute()

        job = job_result.data

        # Get resume
        resume_result = supabase.table("resume_versions")\
            .select("*")\
            .eq("id", request.resume_id)\
            .eq("user_id", user_id)\
            .single()\
            .execute()

        resume = resume_result.data

        # Convert resume structure to text for analysis
        resume_text = _resume_to_text(resume['resume_structure'])

        # Prepare job data for matching
        job_data = {
            "job_title": job['job_title'],
            "company": job['company_name'],
            "ats_system": None,
            "keywords": {
                "all": job['extracted_keywords'],
                "required": job.get('required_skills', []),
                "preferred": job.get('preferred_skills', [])
            }
        }

        # Get ATS system name if available
        if job.get('ats_system_id'):
            ats_result = supabase.table("ats_systems")\
                .select("system_name")\
                .eq("id", job['ats_system_id'])\
                .single()\
                .execute()
            job_data['ats_system'] = ats_result.data['system_name']

        # Calculate match
        match_analysis = await job_matcher.calculate_match_score(
            resume_text=resume_text,
            job_data=job_data
        )

        # Get keyword density analysis
        keyword_density = ats_optimizer.get_keyword_density(
            text=resume_text,
            keywords=job['extracted_keywords']
        )

        return {
            "match_analysis": match_analysis,
            "keyword_density": keyword_density,
            "job_title": job['job_title'],
            "company": job['company_name']
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{job_id}/keywords")
async def get_job_keywords(job_id: str, user_id: str):
    """Get extracted keywords from job posting"""
    try:
        result = supabase.table("job_postings")\
            .select("extracted_keywords, required_skills, preferred_skills")\
            .eq("id", job_id)\
            .eq("user_id", user_id)\
            .single()\
            .execute()

        return {
            "all_keywords": result.data['extracted_keywords'],
            "required": result.data.get('required_skills', []),
            "preferred": result.data.get('preferred_skills', [])
        }

    except Exception as e:
        raise HTTPException(status_code=404, detail="Job posting not found")


@router.delete("/{job_id}")
async def delete_job_posting(job_id: str, user_id: str):
    """Delete a job posting"""
    try:
        supabase.table("job_postings")\
            .delete()\
            .eq("id", job_id)\
            .eq("user_id", user_id)\
            .execute()

        return {"success": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ats-systems/list")
async def list_ats_systems():
    """Get list of all known ATS systems"""
    try:
        result = supabase.table("ats_systems")\
            .select("*")\
            .execute()

        return {"ats_systems": result.data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _resume_to_text(resume_structure: Dict[str, Any]) -> str:
    """Convert resume structure to plain text for analysis"""
    text_parts = []

    # Add contact info
    contact = resume_structure.get('contact_info', {})
    text_parts.append(contact.get('name', ''))

    # Add summary
    text_parts.append(resume_structure.get('summary', ''))

    # Add experience
    for exp in resume_structure.get('experience', []):
        text_parts.append(exp.get('title', ''))
        text_parts.append(exp.get('company', ''))
        for bullet in exp.get('bullets', []):
            text_parts.append(bullet)

    # Add skills
    skills = resume_structure.get('skills', {})
    for category, skill_list in skills.items():
        text_parts.extend(skill_list)

    # Add education
    for edu in resume_structure.get('education', []):
        text_parts.append(edu.get('degree', ''))
        text_parts.append(edu.get('field', ''))
        text_parts.append(edu.get('institution', ''))

    # Add certifications
    for cert in resume_structure.get('certifications', []):
        text_parts.append(cert.get('name', ''))

    return ' '.join(text_parts)
