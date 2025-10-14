"""
Job Matcher Service
Parses job descriptions, extracts keywords, calculates match scores
"""
from typing import Dict, Any, List, Optional
import anthropic
import os
import re
from ..database import get_supabase

class JobMatcher:
    def __init__(self):
        self.claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.supabase = get_supabase()

        # Known ATS systems and their URL patterns
        self.ats_systems = {
            "workday": ["myworkdayjobs.com", "wd1.myworkdayjobs.com", "wd5.myworkdayjobs.com"],
            "greenhouse": ["greenhouse.io", "grnh.se"],
            "lever": ["lever.co", "jobs.lever.co"],
            "icims": ["icims.com"],
            "taleo": ["taleo.net"],
            "smartrecruiters": ["smartrecruiters.com"],
            "jobvite": ["jobvite.com"],
            "bamboohr": ["bamboohr.com"]
        }

    async def parse_job_description(
        self,
        job_description: str,
        job_url: Optional[str] = None,
        company_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Parse job description and extract structured information

        Args:
            job_description: Full text of job posting
            job_url: URL of job posting (for ATS detection)
            company_name: Name of company

        Returns:
            Structured job information with keywords and requirements
        """
        # 1. Detect ATS system from URL
        ats_system = self._detect_ats_system(job_url) if job_url else None

        # 2. Extract keywords using Claude
        keywords = await self._extract_keywords(job_description)

        # 3. Extract requirements
        requirements = await self._extract_requirements(job_description)

        # 4. Extract job title
        job_title = await self._extract_job_title(job_description)

        # 5. Categorize keywords
        categorized_keywords = await self._categorize_keywords(keywords)

        # 6. Extract experience level
        experience_level = self._extract_experience_level(job_description)

        return {
            "job_title": job_title,
            "company": company_name,
            "ats_system": ats_system,
            "keywords": {
                "all": keywords,
                "categorized": categorized_keywords,
                "required": categorized_keywords.get("required", []),
                "preferred": categorized_keywords.get("preferred", [])
            },
            "requirements": requirements,
            "experience_level": experience_level,
            "job_url": job_url,
            "parsed_at": self._get_timestamp()
        }

    async def calculate_match_score(
        self,
        resume_text: str,
        job_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate how well resume matches job requirements

        Args:
            resume_text: Full text of resume
            job_data: Parsed job description data

        Returns:
            Match analysis with score and recommendations
        """
        resume_lower = resume_text.lower()
        all_keywords = job_data['keywords']['all']
        required_keywords = job_data['keywords'].get('required', [])
        preferred_keywords = job_data['keywords'].get('preferred', [])

        # Calculate keyword matches
        matched_required = []
        missing_required = []
        for keyword in required_keywords:
            if keyword.lower() in resume_lower:
                matched_required.append(keyword)
            else:
                missing_required.append(keyword)

        matched_preferred = []
        for keyword in preferred_keywords:
            if keyword.lower() in resume_lower:
                matched_preferred.append(keyword)

        matched_all = []
        missing_all = []
        for keyword in all_keywords:
            if keyword.lower() in resume_lower:
                matched_all.append(keyword)
            else:
                missing_all.append(keyword)

        # Calculate scores
        required_score = (len(matched_required) / len(required_keywords) * 100) if required_keywords else 100
        preferred_score = (len(matched_preferred) / len(preferred_keywords) * 100) if preferred_keywords else 0
        overall_score = (len(matched_all) / len(all_keywords) * 100) if all_keywords else 0

        # Weighted final score (required keywords worth more)
        final_score = (required_score * 0.7) + (preferred_score * 0.2) + (overall_score * 0.1)

        # Get match level
        match_level = self._get_match_level(final_score)

        # Generate recommendations
        recommendations = self._generate_match_recommendations(
            missing_required,
            missing_all,
            final_score
        )

        return {
            "match_score": round(final_score, 1),
            "match_level": match_level,
            "required_match": round(required_score, 1),
            "preferred_match": round(preferred_score, 1),
            "overall_match": round(overall_score, 1),
            "matched_keywords": {
                "required": matched_required,
                "preferred": matched_preferred,
                "all": matched_all
            },
            "missing_keywords": {
                "required": missing_required,
                "all": missing_all[:10]  # Top 10 missing
            },
            "recommendations": recommendations,
            "ats_compatibility": self._get_ats_recommendations(job_data.get('ats_system'))
        }

    async def extract_keywords_with_ai(self, job_description: str) -> Dict[str, List[str]]:
        """
        Enhanced keyword extraction using AI
        Categorizes keywords by importance and type

        Returns:
            Dictionary with categorized keywords:
            {
                "critical": List[str],  # Must-have keywords
                "important": List[str],  # Should-have keywords
                "nice_to_have": List[str],  # Bonus keywords
                "technical": List[str],  # Technical skills
                "soft_skills": List[str]  # Soft skills
            }
        """
        prompt = f"""Analyze this job description and extract the 15 most important keywords.
Categorize them by criticality and type.

Job Description:
{job_description}

Return in this EXACT JSON format:
{{
  "critical": ["keyword1", "keyword2"],
  "important": ["keyword3", "keyword4"],
  "nice_to_have": ["keyword5", "keyword6"],
  "technical": ["Python", "AWS"],
  "soft_skills": ["leadership", "communication"]
}}

Rules:
1. Critical: Skills mentioned multiple times or in "required" sections
2. Important: Skills in "preferred" or "responsibilities" sections
3. Nice to have: Skills mentioned once or as "plus"
4. Technical: Programming languages, tools, technologies
5. Soft skills: Communication, leadership, teamwork, etc.

Return ONLY valid JSON, no markdown."""

        message = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text.strip()

        # Clean JSON
        if response_text.startswith('```json'):
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif response_text.startswith('```'):
            response_text = response_text.split('```')[1].split('```')[0].strip()

        import json
        categorized_keywords = json.loads(response_text)

        return categorized_keywords

    async def categorize_requirements(self, job_description: str) -> Dict[str, Any]:
        """
        Categorize job requirements into MUST_HAVE vs NICE_TO_HAVE
        More sophisticated than simple extraction

        Returns:
            {
                "must_have": {
                    "skills": List[str],
                    "experience_years": int or None,
                    "education": str or None,
                    "certifications": List[str]
                },
                "nice_to_have": {
                    "skills": List[str],
                    "experience_areas": List[str],
                    "certifications": List[str]
                },
                "deal_breakers": List[str]  # Hard requirements that auto-reject
            }
        """
        prompt = f"""Analyze this job description and categorize ALL requirements.

Job Description:
{job_description}

Identify:
1. MUST HAVE requirements (will auto-reject if missing)
2. NICE TO HAVE requirements (preferred but not required)
3. Deal breakers (explicit requirements like "must have US work authorization")

Return in this EXACT JSON format:
{{
  "must_have": {{
    "skills": ["skill1", "skill2"],
    "experience_years": 5,
    "education": "Bachelor's degree in Computer Science",
    "certifications": ["AWS Certified"]
  }},
  "nice_to_have": {{
    "skills": ["skill3", "skill4"],
    "experience_areas": ["fintech", "startup"],
    "certifications": ["PMP"]
  }},
  "deal_breakers": ["Must be authorized to work in US", "Must pass background check"]
}}

Return ONLY valid JSON, no markdown."""

        message = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text.strip()

        # Clean JSON
        if response_text.startswith('```json'):
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif response_text.startswith('```'):
            response_text = response_text.split('```')[1].split('```')[0].strip()

        import json
        categorized_reqs = json.loads(response_text)

        return categorized_reqs

    async def _extract_keywords(self, job_description: str) -> List[str]:
        """
        Extract key terms from job description (legacy method)
        Use extract_keywords_with_ai() for enhanced extraction
        """
        prompt = f"""Extract 15-25 of the most important keywords from this job description.

Focus on:
1. Technical skills and tools
2. Soft skills
3. Certifications
4. Industry terminology
5. Job title variations
6. Required qualifications

Job Description:
{job_description}

Return ONLY a comma-separated list of keywords."""

        message = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        keywords_text = message.content[0].text
        keywords = [k.strip() for k in keywords_text.split(',')]

        return keywords

    async def _extract_requirements(self, job_description: str) -> Dict[str, List[str]]:
        """Extract required vs preferred qualifications"""
        prompt = f"""Analyze this job description and separate requirements into two categories:

1. REQUIRED qualifications (must-haves)
2. PREFERRED qualifications (nice-to-haves)

Job Description:
{job_description}

Return in this exact format:
REQUIRED:
- requirement 1
- requirement 2

PREFERRED:
- preference 1
- preference 2"""

        message = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )

        response = message.content[0].text

        # Parse response
        required = []
        preferred = []

        current_section = None
        for line in response.split('\n'):
            line = line.strip()
            if line.startswith('REQUIRED'):
                current_section = 'required'
            elif line.startswith('PREFERRED'):
                current_section = 'preferred'
            elif line.startswith('-') or line.startswith('•'):
                item = line.lstrip('-•').strip()
                if current_section == 'required':
                    required.append(item)
                elif current_section == 'preferred':
                    preferred.append(item)

        return {
            "required": required,
            "preferred": preferred
        }

    async def _extract_job_title(self, job_description: str) -> str:
        """Extract job title from description"""
        # Try to find title in first few lines
        lines = job_description.split('\n')[:5]

        for line in lines:
            # Common patterns
            if 'position:' in line.lower() or 'job title:' in line.lower():
                return line.split(':', 1)[1].strip()
            # If line is short and title-like
            if len(line.split()) <= 5 and len(line) < 50:
                return line.strip()

        # Fall back to Claude if no clear title found
        prompt = f"""What is the job title for this position? Return ONLY the job title, nothing else.

{job_description[:500]}"""

        message = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=50,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text.strip()

    async def _categorize_keywords(self, keywords: List[str]) -> Dict[str, List[str]]:
        """Categorize keywords into technical, soft skills, etc."""
        keywords_text = ", ".join(keywords)

        prompt = f"""Categorize these keywords into: technical_skills, soft_skills, tools, certifications, other.

Keywords: {keywords_text}

Return in this format:
technical_skills: keyword1, keyword2
soft_skills: keyword3, keyword4
tools: keyword5
certifications: keyword6
other: keyword7"""

        message = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        response = message.content[0].text

        # Parse categorized keywords
        categorized = {}
        for line in response.split('\n'):
            if ':' in line:
                category, items = line.split(':', 1)
                category = category.strip()
                keyword_list = [k.strip() for k in items.split(',') if k.strip()]
                if keyword_list:
                    categorized[category] = keyword_list

        return categorized

    def _extract_experience_level(self, job_description: str) -> str:
        """Detect experience level from job description"""
        desc_lower = job_description.lower()

        # Entry level indicators
        if any(term in desc_lower for term in ['entry level', '0-2 years', 'recent graduate', 'junior']):
            return "entry_level"

        # Senior level indicators
        if any(term in desc_lower for term in ['senior', '10+ years', '8+ years', 'lead', 'principal']):
            return "senior"

        # Mid level indicators
        if any(term in desc_lower for term in ['3-5 years', '5-7 years', 'mid-level', 'intermediate']):
            return "mid_level"

        # Executive indicators
        if any(term in desc_lower for term in ['director', 'vp', 'vice president', 'executive', 'c-level', 'chief']):
            return "executive"

        return "not_specified"

    def _detect_ats_system(self, job_url: str) -> Optional[str]:
        """Detect ATS system from job posting URL"""
        if not job_url:
            return None

        url_lower = job_url.lower()

        for ats_name, patterns in self.ats_systems.items():
            for pattern in patterns:
                if pattern in url_lower:
                    return ats_name

        return None

    def _get_match_level(self, score: float) -> str:
        """Convert score to match level"""
        if score >= 80:
            return "excellent"
        elif score >= 70:
            return "good"
        elif score >= 60:
            return "fair"
        elif score >= 50:
            return "weak"
        else:
            return "poor"

    def _generate_match_recommendations(
        self,
        missing_required: List[str],
        missing_all: List[str],
        score: float
    ) -> List[str]:
        """Generate recommendations to improve match"""
        recommendations = []

        if missing_required:
            recommendations.append(
                f"CRITICAL: Add these required keywords: {', '.join(missing_required[:5])}"
            )

        if score < 75:
            recommendations.append(
                f"Target 75%+ match rate. Currently at {score:.1f}%. Add {len(missing_all[:10])} more keywords."
            )

        if score >= 75:
            recommendations.append(
                "Good match! Consider tailoring bullet points to emphasize matched skills."
            )

        if missing_all:
            top_missing = missing_all[:5]
            recommendations.append(
                f"Consider adding if applicable: {', '.join(top_missing)}"
            )

        return recommendations

    def _get_ats_recommendations(self, ats_system: Optional[str]) -> List[str]:
        """Get system-specific ATS recommendations"""
        if not ats_system:
            return ["Use standard ATS-friendly format (DOCX recommended)"]

        recommendations = []

        if ats_system == "workday":
            recommendations.extend([
                "Use 'Apply with LinkedIn' for fastest application",
                "Create separate Workday profile for this employer",
                "Answer knockout questions carefully - they auto-reject"
            ])
        elif ats_system == "greenhouse":
            recommendations.extend([
                "Greenhouse has modern parsing - PDF acceptable",
                "Clean, simple format works best",
                "System handles referrals well"
            ])
        elif ats_system == "taleo":
            recommendations.extend([
                "Use DOCX format (Taleo struggles with PDFs)",
                "Keep formatting extremely simple",
                "Avoid any special characters or symbols"
            ])
        elif ats_system == "lever":
            recommendations.extend([
                "Lever emphasizes relationships - mention referrals",
                "Modern system handles standard PDFs well",
                "Include portfolio link if relevant"
            ])
        elif ats_system == "icims":
            recommendations.extend([
                "Use traditional DOCX format",
                "Keep layout simple - older parsing technology",
                "Ensure consistent date formatting"
            ])

        return recommendations

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat()

    async def store_job_posting(
        self,
        user_id: str,
        job_data: Dict[str, Any],
        job_description_full: str
    ) -> str:
        """
        Store job posting in database

        Returns job posting ID
        """
        # Detect ATS system ID from database
        ats_system_id = None
        if job_data.get('ats_system'):
            ats_result = self.supabase.table("ats_systems")\
                .select("id")\
                .eq("system_name", job_data['ats_system'])\
                .execute()

            if ats_result.data:
                ats_system_id = ats_result.data[0]['id']

        # Store job posting
        job_record = {
            "user_id": user_id,
            "job_title": job_data.get('job_title'),
            "company_name": job_data.get('company'),
            "job_url": job_data.get('job_url'),
            "job_description": job_description_full,
            "extracted_keywords": job_data['keywords']['all'],
            "required_skills": job_data['keywords'].get('required', []),
            "preferred_skills": job_data['keywords'].get('preferred', []),
            "ats_system_id": ats_system_id
        }

        result = self.supabase.table("job_postings").insert(job_record).execute()

        return result.data[0]['id']

    async def get_user_job_postings(self, user_id: str) -> List[Dict]:
        """Get all job postings for a user"""
        result = self.supabase.table("job_postings")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("created_at", desc=True)\
            .execute()

        return result.data
