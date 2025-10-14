"""
Company Research Service
Automatically researches companies to gather information for resume tailoring
"""
from typing import Dict, Any, Optional, List
import anthropic
import os
import re
from dotenv import load_dotenv

load_dotenv()

class CompanyResearchService:
    """
    Researches companies using web search and AI analysis
    Extracts company values, culture, and key information for resume tailoring
    """

    def __init__(self):
        self.claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    async def research_company(
        self,
        company_name: str,
        job_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Research a company and extract relevant information

        Args:
            company_name: Name of the company
            job_url: Optional URL of the job posting

        Returns:
            Dictionary with company information:
            {
                "company_name": str,
                "website": str or None,
                "linkedin": str or None,
                "about": str or None,
                "values": List[str],
                "culture_keywords": List[str],
                "industry": str or None,
                "size": str or None,
                "locations": List[str],
                "research_success": bool,
                "error": str or None
            }
        """

        try:
            # Step 1: Find company website
            website = await self._find_company_website(company_name)

            # Step 2: Find LinkedIn profile
            linkedin = await self._find_linkedin_profile(company_name)

            # Step 3: If website found, extract "About Us" information
            about_text = None
            if website:
                about_text = await self._extract_about_section(website, company_name)

            # Step 4: Extract structured information using AI
            company_info = await self._analyze_company_info(
                company_name=company_name,
                about_text=about_text,
                website=website,
                linkedin=linkedin,
                job_url=job_url
            )

            return {
                "company_name": company_name,
                "website": website,
                "linkedin": linkedin,
                "about": about_text,
                "values": company_info.get("values", []),
                "culture_keywords": company_info.get("culture_keywords", []),
                "industry": company_info.get("industry"),
                "size": company_info.get("size"),
                "locations": company_info.get("locations", []),
                "research_success": True,
                "error": None
            }

        except Exception as e:
            print(f"Error researching company {company_name}: {str(e)}")
            return {
                "company_name": company_name,
                "website": None,
                "linkedin": None,
                "about": None,
                "values": [],
                "culture_keywords": [],
                "industry": None,
                "size": None,
                "locations": [],
                "research_success": False,
                "error": str(e)
            }

    async def _find_company_website(self, company_name: str) -> Optional[str]:
        """
        Find company website using web search simulation
        In production, this would use actual web search API
        """

        # Simulate search query
        search_query = f"{company_name} official website"

        # Use Claude to infer likely website URL
        prompt = f"""Given the company name "{company_name}", what is the most likely official website URL?

Return ONLY the URL in this format: https://www.example.com

If you're not confident, return: UNKNOWN

Common patterns:
- Company Name Inc -> https://www.companyname.com
- Acme Corp -> https://www.acme.com
- Tech Startup -> https://www.techstartup.io

Company: {company_name}
URL:"""

        try:
            message = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}]
            )

            url = message.content[0].text.strip()

            if url == "UNKNOWN" or not url.startswith("http"):
                return None

            return url

        except Exception as e:
            print(f"Error finding website for {company_name}: {str(e)}")
            return None

    async def _find_linkedin_profile(self, company_name: str) -> Optional[str]:
        """
        Find company LinkedIn profile
        Simulates search: "company_name site:linkedin.com/company"
        """

        # Use Claude to construct likely LinkedIn URL
        prompt = f"""Given the company name "{company_name}", construct the most likely LinkedIn company page URL.

Format: https://www.linkedin.com/company/company-slug

Rules:
- Convert company name to lowercase
- Replace spaces with hyphens
- Remove special characters (Inc, Corp, LLC, etc.)
- Remove punctuation

Examples:
- "Acme Corporation" -> https://www.linkedin.com/company/acme
- "Tech Startup Inc." -> https://www.linkedin.com/company/tech-startup
- "ABC & Associates" -> https://www.linkedin.com/company/abc-associates

Company: {company_name}
LinkedIn URL:"""

        try:
            message = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}]
            )

            linkedin_url = message.content[0].text.strip()

            if not linkedin_url.startswith("https://www.linkedin.com/company/"):
                return None

            return linkedin_url

        except Exception as e:
            print(f"Error finding LinkedIn for {company_name}: {str(e)}")
            return None

    async def _extract_about_section(
        self,
        website: str,
        company_name: str
    ) -> Optional[str]:
        """
        Extract "About Us" section from company website

        In production, this would:
        1. Fetch the website HTML
        2. Find the About/About Us/Company page
        3. Extract relevant text

        For now, we simulate this with AI knowledge
        """

        prompt = f"""Based on your knowledge, provide a brief "About" section for {company_name} (website: {website}).

Include:
- What the company does
- Their mission or purpose
- When they were founded (if notable)
- Industry they operate in

Keep it to 2-3 sentences. If you don't have information, return: UNKNOWN"""

        try:
            message = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )

            about_text = message.content[0].text.strip()

            if about_text == "UNKNOWN":
                return None

            return about_text

        except Exception as e:
            print(f"Error extracting about section for {company_name}: {str(e)}")
            return None

    async def _analyze_company_info(
        self,
        company_name: str,
        about_text: Optional[str],
        website: Optional[str],
        linkedin: Optional[str],
        job_url: Optional[str]
    ) -> Dict[str, Any]:
        """
        Use AI to extract structured information about the company
        """

        context = f"""Company: {company_name}
Website: {website or 'Not found'}
LinkedIn: {linkedin or 'Not found'}
About: {about_text or 'Not available'}
Job URL: {job_url or 'Not provided'}"""

        prompt = f"""Analyze this company information and extract structured data.

{context}

Extract:
1. Core values (look for keywords like: innovation, integrity, excellence, collaboration, customer-first, etc.)
2. Culture keywords (e.g., fast-paced, remote-friendly, data-driven, entrepreneurial, etc.)
3. Industry
4. Company size (startup, small, medium, large, enterprise)
5. Known locations/headquarters

Return in this EXACT JSON format:
{{
  "values": ["value1", "value2", "value3"],
  "culture_keywords": ["keyword1", "keyword2", "keyword3"],
  "industry": "Industry name",
  "size": "small/medium/large/enterprise",
  "locations": ["City, State", "City, State"]
}}

If information is not available, use empty arrays or null.
Return ONLY valid JSON, no markdown or explanation."""

        try:
            message = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text.strip()

            # Clean JSON if wrapped in code blocks
            if response_text.startswith('```json'):
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif response_text.startswith('```'):
                response_text = response_text.split('```')[1].split('```')[0].strip()

            import json
            company_data = json.loads(response_text)

            return company_data

        except Exception as e:
            print(f"Error analyzing company info for {company_name}: {str(e)}")
            return {
                "values": [],
                "culture_keywords": [],
                "industry": None,
                "size": None,
                "locations": []
            }

    def get_tailoring_suggestions(
        self,
        company_research: Dict[str, Any]
    ) -> List[str]:
        """
        Generate suggestions for how to tailor resume based on company research

        Args:
            company_research: Output from research_company()

        Returns:
            List of actionable suggestions
        """

        suggestions = []

        # Suggestions based on values
        if company_research.get("values"):
            values_str = ", ".join(company_research["values"][:3])
            suggestions.append(
                f"Emphasize alignment with company values: {values_str}"
            )

        # Suggestions based on culture
        if company_research.get("culture_keywords"):
            culture_str = ", ".join(company_research["culture_keywords"][:3])
            suggestions.append(
                f"Highlight experience in {culture_str} environments"
            )

        # Suggestions based on industry
        if company_research.get("industry"):
            suggestions.append(
                f"Emphasize {company_research['industry']} industry experience or transferable skills"
            )

        # Suggestions based on company size
        size = company_research.get("size")
        if size == "startup":
            suggestions.append(
                "Highlight versatility, ability to wear multiple hats, and startup experience"
            )
        elif size == "enterprise":
            suggestions.append(
                "Emphasize experience with large-scale systems, cross-team collaboration, and enterprise processes"
            )

        return suggestions


# Singleton instance
company_research_service = CompanyResearchService()
