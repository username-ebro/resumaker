"""
Jobs Router
API endpoints for job posting management and keyword analysis
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from ..services.job_matcher import JobMatcher
from ..services.ats_optimizer import ATSOptimizer
from ..services.web_scraper_service import WebScraperService
from ..services.company_research_service import company_research_service
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

class CreateJobRequest(BaseModel):
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    description: str
    url: Optional[str] = None
    requirements: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    ats_system: Optional[str] = None
    company_info: Optional[Dict[str, Any]] = None

# Initialize services
job_matcher = JobMatcher()
ats_optimizer = ATSOptimizer()
web_scraper = WebScraperService()
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
        resume_text = _resume_to_text(resume['content'])

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


@router.post("/analyze")
async def analyze_job_posting(
    request: AddJobRequest,
    user_id: str
):
    """
    Analyze a job posting and extract all key information

    Extracts:
    - Required skills
    - Preferred skills
    - Keywords for ATS optimization
    - Key responsibilities
    - ATS system detection
    - Company information (if URL provided)

    Can fetch from URL or use provided job_description text.
    Stores in database and returns structured analysis.
    """
    try:
        job_description = request.job_description
        company_name = request.company_name
        location = None
        scraped_data = None

        # If URL provided, try to scrape it first (but prefer user-provided text)
        if request.job_url:
            print(f"Scraping job posting from URL: {request.job_url}")
            scraped_data = await web_scraper.scrape_job_posting(request.job_url)

            if scraped_data.get('success'):
                # ONLY use scraped text if no description was provided
                if scraped_data.get('text') and not job_description:
                    job_description = scraped_data['text']
                    print(f"Using scraped text ({len(job_description)} chars)")
                elif job_description:
                    print(f"Using user-provided description ({len(job_description)} chars), ignoring scraped text")

                # Use scraped company if not provided
                if scraped_data.get('company') and not company_name:
                    company_name = scraped_data['company']
                    print(f"Using scraped company: {company_name}")

                # Extract location
                if scraped_data.get('location'):
                    location = scraped_data['location']
                    print(f"Using scraped location: {location}")
            else:
                print(f"Scraping failed: {scraped_data.get('error')}")

        # Parse job description with full analysis
        job_data = await job_matcher.parse_job_description(
            job_description=job_description,
            job_url=request.job_url,
            company_name=company_name
        )

        # Merge scraped keywords if available
        if scraped_data and scraped_data.get('keywords'):
            # Combine and deduplicate keywords
            all_keywords = list(set(job_data['keywords']['all'] + scraped_data['keywords']))
            job_data['keywords']['all'] = all_keywords[:25]  # Limit to 25
            print(f"Merged keywords: {len(all_keywords)} unique keywords")

        # Merge scraped requirements if available
        if scraped_data and scraped_data.get('requirements'):
            scraped_reqs = scraped_data['requirements']
            if scraped_reqs.get('required'):
                job_data['requirements']['required'].extend(scraped_reqs['required'])
            if scraped_reqs.get('preferred'):
                job_data['requirements']['preferred'].extend(scraped_reqs['preferred'])
            print("Merged scraped requirements")

        # Detect ATS system if URL provided
        ats_system_id = None
        ats_system_name = None
        if job_data.get('ats_system'):
            ats_result = supabase.table("ats_systems")\
                .select("id, name")\
                .ilike("name", f"%{job_data['ats_system']}%")\
                .limit(1)\
                .execute()

            if ats_result.data:
                ats_system_id = ats_result.data[0]['id']
                ats_system_name = ats_result.data[0]['name']

        # Store in database
        job_record = {
            "user_id": user_id,
            "job_title": job_data.get('job_title'),
            "company_name": company_name,
            "job_url": request.job_url,
            "job_description": job_description,
            "extracted_keywords": job_data['keywords']['all'],
            "required_skills": job_data['keywords'].get('required', []),
            "preferred_skills": job_data['keywords'].get('preferred', []),
            "ats_system_id": ats_system_id
        }

        result = supabase.table("job_postings").insert(job_record).execute()
        job_id = result.data[0]['id']

        # Research company in background (don't block response)
        company_info_result = {"website": None, "linkedin": None, "values": [], "about": None}
        if company_name:
            try:
                print(f"Researching company: {company_name}")
                company_research = await company_research_service.research_company(
                    company_name=company_name,
                    job_url=request.job_url
                )
                if company_research.get('research_success'):
                    company_info_result = {
                        "website": company_research.get('website'),
                        "linkedin": company_research.get('linkedin'),
                        "values": company_research.get('values', []),
                        "about": company_research.get('about')
                    }
                    print(f"✅ Company research successful for {company_name}")
                else:
                    print(f"⚠️ Company research failed: {company_research.get('error')}")
            except Exception as e:
                print(f"Company research error (non-fatal): {str(e)}")
                # Don't fail the whole request if company research fails

        # Format for frontend JobConfirmation component
        return {
            "success": True,
            "job_id": job_id,
            "job_data": {
                "title": job_data.get('job_title'),
                "company": company_name,
                "location": location,
                "description": job_description,
                "url": request.job_url,
                "ats_system": ats_system_name,
                "keywords": job_data['keywords']['all'][:15],  # Top 15 keywords for display
                "requirements": (
                    job_data.get('requirements', {}).get('required', []) +
                    job_data.get('requirements', {}).get('preferred', [])
                )[:10],  # Top 10 requirements
                "company_info": company_info_result
            },
            # Keep full analysis for internal use
            "analysis": {
                "job_title": job_data.get('job_title'),
                "company": company_name,
                "location": location,
                "ats_system_detected": ats_system_name,
                "ats_system_id": ats_system_id,
                "keywords": job_data['keywords'],
                "requirements": job_data.get('requirements', {}),
                "experience_level": job_data.get('experience_level'),
                "keyword_count": len(job_data['keywords']['all']),
                "required_count": len(job_data['keywords'].get('required', [])),
                "preferred_count": len(job_data['keywords'].get('preferred', [])),
                "scraped": bool(scraped_data and scraped_data.get('success'))
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job analysis failed: {str(e)}")


@router.post("/create")
async def create_job_posting(
    request: CreateJobRequest,
    user_id: str
):
    """
    Create a new job posting manually

    Accepts all job fields directly without analysis.
    Use this endpoint when you already have structured data.
    For automatic analysis, use /jobs/analyze instead.
    """
    try:
        # Find ATS system ID if name provided
        ats_system_id = None
        if request.ats_system:
            ats_result = supabase.table("ats_systems")\
                .select("id")\
                .ilike("system_name", f"%{request.ats_system}%")\
                .limit(1)\
                .execute()

            if ats_result.data:
                ats_system_id = ats_result.data[0]['id']

        # Create job record
        job_record = {
            "user_id": user_id,
            "job_title": request.title,
            "company_name": request.company,
            "job_url": request.url,
            "job_description": request.description,
            "extracted_keywords": request.keywords or [],
            "required_skills": request.requirements or [],
            "preferred_skills": [],  # Could separate from requirements if needed
            "ats_system_id": ats_system_id
        }

        result = supabase.table("job_postings").insert(job_record).execute()
        job_id = result.data[0]['id']

        return {
            "success": True,
            "job_id": job_id,
            "job": result.data[0]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create job posting: {str(e)}")


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
