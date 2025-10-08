"""Import Parser - Extract resume data from ChatGPT/Claude conversations"""

from anthropic import Anthropic
import os
from dotenv import load_dotenv
import json

load_dotenv()

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

class ImportParser:
    def __init__(self):
        self.client = Anthropic(api_key=CLAUDE_API_KEY)

    async def parse_conversation(self, conversation_text: str, source_platform: str = "unknown") -> dict:
        """Parse a conversation and extract resume-relevant data"""

        prompt = f"""I have a conversation from {source_platform} that contains information about someone's professional background.

Your task: Extract ALL resume-relevant information from this conversation.

Look for:
- Job titles, companies, dates of employment
- Specific accomplishments with metrics (increased X by Y%, managed $Z budget, etc.)
- Skills mentioned (technical, soft skills, languages)
- Education, certifications, awards
- Projects and their outcomes
- Anecdotes that demonstrate skills or achievements
- Any other career-relevant information

Conversation:
{conversation_text}

Return a JSON object with this structure:
{{
  "accomplishments": [
    {{
      "description": "Full description of accomplishment",
      "metrics": ["any quantifiable results"],
      "company": "if mentioned",
      "timeframe": "if mentioned",
      "skills_demonstrated": ["list of skills"]
    }}
  ],
  "skills": {{
    "technical": [],
    "soft_skills": [],
    "languages": []
  }},
  "experience": [
    {{
      "company": "",
      "title": "",
      "dates": "",
      "responsibilities": [],
      "achievements": []
    }}
  ],
  "education": [],
  "certifications": [],
  "projects": [
    {{
      "name": "",
      "description": "",
      "technologies": [],
      "outcomes": []
    }}
  ],
  "stories": [
    {{
      "situation": "",
      "action": "",
      "result": "",
      "skills_demonstrated": []
    }}
  ]
}}

Be thorough - extract EVERYTHING that could be useful for a resume."""

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text

        # Clean up JSON
        if response_text.startswith('```json'):
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif response_text.startswith('```'):
            response_text = response_text.split('```')[1].split('```')[0].strip()

        return json.loads(response_text)

# Singleton
import_parser = ImportParser()
