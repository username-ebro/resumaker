"""
Web Scraper Service
Fetches and parses job postings from URLs
"""
from typing import Optional, Dict, Any, List
import requests
from bs4 import BeautifulSoup
import re
import anthropic
import os
from urllib.parse import urlparse


class WebScraperService:
    def __init__(self):
        self.claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        # User-Agent to avoid blocks
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

        self.timeout = 10  # seconds

    def fetch_url_content(self, url: str) -> Optional[str]:
        """
        Fetch HTML content from URL

        Args:
            url: Job posting URL

        Returns:
            HTML content as string, or None if error
        """
        try:
            print(f"Fetching URL: {url}")
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout,
                allow_redirects=True
            )

            # Check for successful response
            if response.status_code == 200:
                print(f"Successfully fetched URL (status: {response.status_code})")
                return response.text
            else:
                print(f"Failed to fetch URL: Status {response.status_code}")
                return None

        except requests.Timeout:
            print(f"Timeout while fetching URL: {url}")
            return None
        except requests.ConnectionError:
            print(f"Connection error while fetching URL: {url}")
            return None
        except requests.RequestException as e:
            print(f"Request error while fetching URL: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error fetching URL: {str(e)}")
            return None

    def extract_text_from_html(self, html: str) -> str:
        """
        Extract clean text from HTML using BeautifulSoup

        Args:
            html: Raw HTML string

        Returns:
            Clean text content
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')

            # Remove script, style, and other unwanted tags
            for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                tag.decompose()

            # Get text and clean it up
            text = soup.get_text(separator='\n', strip=True)

            # Remove excessive whitespace
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            text = '\n'.join(lines)

            # Remove multiple consecutive blank lines
            text = re.sub(r'\n{3,}', '\n\n', text)

            print(f"Extracted {len(text)} characters of text from HTML")
            return text

        except Exception as e:
            print(f"Error extracting text from HTML: {str(e)}")
            return ""

    async def extract_company_from_text(self, text: str, job_title: Optional[str] = None) -> Optional[str]:
        """
        Extract company name from job posting text using Claude

        Args:
            text: Job posting text
            job_title: Optional job title for context

        Returns:
            Company name or None
        """
        try:
            # Truncate text if too long (use first 2000 chars which usually has company info)
            text_sample = text[:2000]

            prompt = f"""Extract the company name from this job posting. Return ONLY the company name, nothing else.

Job Title: {job_title or 'Unknown'}

Job Posting Text:
{text_sample}

Company Name:"""

            message = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=50,
                messages=[{"role": "user", "content": prompt}]
            )

            company_name = message.content[0].text.strip()
            print(f"Extracted company name: {company_name}")
            return company_name if company_name and company_name.lower() != 'unknown' else None

        except Exception as e:
            print(f"Error extracting company name: {str(e)}")
            return None

    async def extract_location(self, text: str) -> Optional[str]:
        """
        Extract location from job posting text

        Args:
            text: Job posting text

        Returns:
            Location string or None
        """
        try:
            # Common location patterns
            location_patterns = [
                r'Location[:\s]+([A-Z][^,\n]+(?:,\s*[A-Z]{2})?)',  # Location: City, ST
                r'(?:City|Location)[:\s]+([A-Z][^,\n]+)',
                r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?,\s*[A-Z]{2})',  # City, ST format
            ]

            for pattern in location_patterns:
                match = re.search(pattern, text[:2000])
                if match:
                    location = match.group(1).strip()
                    print(f"Extracted location: {location}")
                    return location

            # Fall back to Claude if patterns don't work
            text_sample = text[:2000]

            prompt = f"""Extract the job location from this job posting. Return ONLY the location (city and state/country), nothing else. If remote, return "Remote". If not found, return "Not specified".

Job Posting Text:
{text_sample}

Location:"""

            message = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=50,
                messages=[{"role": "user", "content": prompt}]
            )

            location = message.content[0].text.strip()
            print(f"Extracted location via Claude: {location}")
            return location if location.lower() != 'not specified' else None

        except Exception as e:
            print(f"Error extracting location: {str(e)}")
            return None

    async def extract_requirements(self, text: str) -> Dict[str, List[str]]:
        """
        Parse requirements and qualifications from job text

        Args:
            text: Job posting text

        Returns:
            Dictionary with 'required' and 'preferred' lists
        """
        try:
            # Truncate to reasonable length for analysis
            text_sample = text[:5000]

            prompt = f"""Analyze this job posting and extract the requirements. Separate them into:
1. REQUIRED qualifications (must-haves, deal-breakers)
2. PREFERRED qualifications (nice-to-haves, bonuses)

Job Posting:
{text_sample}

Return in this exact format:
REQUIRED:
- requirement 1
- requirement 2

PREFERRED:
- preference 1
- preference 2

Be specific and extract actual requirements, not generic statements."""

            message = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            response = message.content[0].text

            # Parse response
            required = []
            preferred = []

            current_section = None
            for line in response.split('\n'):
                line = line.strip()
                if line.upper().startswith('REQUIRED'):
                    current_section = 'required'
                elif line.upper().startswith('PREFERRED'):
                    current_section = 'preferred'
                elif line.startswith('-') or line.startswith('•'):
                    item = line.lstrip('-•').strip()
                    if current_section == 'required':
                        required.append(item)
                    elif current_section == 'preferred':
                        preferred.append(item)

            print(f"Extracted {len(required)} required and {len(preferred)} preferred requirements")

            return {
                "required": required,
                "preferred": preferred
            }

        except Exception as e:
            print(f"Error extracting requirements: {str(e)}")
            return {"required": [], "preferred": []}

    async def extract_keywords(self, text: str) -> List[str]:
        """
        Extract important keywords from job posting

        Args:
            text: Job posting text

        Returns:
            List of 10-15 important keywords
        """
        try:
            # Truncate to reasonable length
            text_sample = text[:5000]

            prompt = f"""Extract the 10-15 most important keywords from this job posting.

Focus on:
1. Technical skills and tools
2. Required qualifications
3. Key technologies
4. Important certifications
5. Core competencies
6. Industry terminology

Job Posting:
{text_sample}

Return ONLY a comma-separated list of keywords, nothing else."""

            message = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )

            keywords_text = message.content[0].text.strip()
            keywords = [k.strip() for k in keywords_text.split(',') if k.strip()]

            print(f"Extracted {len(keywords)} keywords")
            return keywords[:15]  # Limit to 15

        except Exception as e:
            print(f"Error extracting keywords: {str(e)}")
            return []

    def get_domain(self, url: str) -> Optional[str]:
        """
        Extract domain from URL for ATS detection

        Args:
            url: Full URL

        Returns:
            Domain name
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            print(f"Extracted domain: {domain}")
            return domain
        except Exception as e:
            print(f"Error extracting domain: {str(e)}")
            return None

    async def scrape_job_posting(self, url: str) -> Dict[str, Any]:
        """
        Complete job posting scraping pipeline

        Args:
            url: Job posting URL

        Returns:
            Dictionary with extracted job data
        """
        result = {
            "success": False,
            "url": url,
            "html": None,
            "text": None,
            "company": None,
            "location": None,
            "requirements": {"required": [], "preferred": []},
            "keywords": [],
            "domain": None,
            "error": None
        }

        try:
            # 1. Fetch HTML
            html = self.fetch_url_content(url)
            if not html:
                result["error"] = "Failed to fetch URL"
                return result

            result["html"] = html

            # 2. Extract text
            text = self.extract_text_from_html(html)
            if not text:
                result["error"] = "Failed to extract text from HTML"
                return result

            result["text"] = text

            # 3. Extract domain
            result["domain"] = self.get_domain(url)

            # 4. Extract structured data (in parallel would be better, but sequential is fine)
            result["company"] = await self.extract_company_from_text(text)
            result["location"] = await self.extract_location(text)
            result["requirements"] = await self.extract_requirements(text)
            result["keywords"] = await self.extract_keywords(text)

            result["success"] = True
            print(f"Successfully scraped job posting from {url}")

        except Exception as e:
            result["error"] = f"Scraping error: {str(e)}"
            print(f"Error in scrape_job_posting: {str(e)}")

        return result
