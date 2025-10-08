"""OCR Service - Resume text extraction using Gemini"""

import google.generativeai as genai
import base64
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

class OCRService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    async def extract_resume_text(self, file_path: str) -> dict:
        """Extract all text and data from a resume image/PDF"""

        # Read file and convert to base64
        with open(file_path, 'rb') as f:
            file_data = f.read()

        base64_data = base64.b64encode(file_data).decode('utf-8')

        # Determine MIME type
        file_ext = Path(file_path).suffix.lower()
        mime_type_map = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.pdf': 'application/pdf'
        }
        mime_type = mime_type_map.get(file_ext, 'application/octet-stream')

        prompt = """Extract ALL information from this resume with 100% accuracy.

Pay special attention to:
- Full name and contact information
- Professional summary/objective
- Work experience (company, title, dates, responsibilities, accomplishments)
- Education (school, degree, dates, GPA if present)
- Skills (technical, soft skills, languages)
- Certifications and awards
- Projects and publications
- Any quantifiable metrics (percentages, dollar amounts, numbers)

Return ONLY a JSON object with this structure:
{
  "personal_info": {
    "name": "",
    "email": "",
    "phone": "",
    "location": "",
    "linkedin": "",
    "website": ""
  },
  "summary": "",
  "experience": [
    {
      "company": "",
      "title": "",
      "start_date": "",
      "end_date": "",
      "location": "",
      "responsibilities": [],
      "accomplishments": []
    }
  ],
  "education": [
    {
      "school": "",
      "degree": "",
      "field": "",
      "start_date": "",
      "end_date": "",
      "gpa": ""
    }
  ],
  "skills": {
    "technical": [],
    "languages": [],
    "soft_skills": []
  },
  "certifications": [],
  "awards": [],
  "projects": []
}

Extract EVERYTHING you see. Do not summarize or interpret - extract exactly as written."""

        # Generate content
        result = self.model.generate_content([
            {
                "inline_data": {
                    "mime_type": mime_type,
                    "data": base64_data
                }
            },
            prompt
        ])

        response_text = result.text

        # Clean up JSON (remove markdown code blocks if present)
        if response_text.startswith('```json'):
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif response_text.startswith('```'):
            response_text = response_text.split('```')[1].split('```')[0].strip()

        import json
        return json.loads(response_text)

# Create singleton instance
ocr_service = OCRService()
