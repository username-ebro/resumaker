"""Reference Request Service - Generate shareable prompts for external validation"""

import uuid
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

FRONTEND_URL = os.getenv("NEXT_PUBLIC_APP_URL", "http://localhost:3000")

class ReferenceService:
    def __init__(self):
        self.base_questions = [
            "What accomplishments or achievements stand out from working with this person?",
            "What skills did you observe them demonstrate?",
            "Can you share a specific example of their work or impact?",
            "What would you say are their key strengths?"
        ]

    async def generate_reference_request(
        self,
        user_id: str,
        target_role: str,
        reference_type: str = "colleague"
    ) -> dict:
        """Generate a shareable reference request"""

        # Generate unique token
        share_token = str(uuid.uuid4())[:8]
        share_url = f"{FRONTEND_URL}/reference/{share_token}"

        # Role-specific questions
        role_questions = []
        if "manager" in reference_type.lower():
            role_questions = [
                "How would you describe their performance and growth?",
                "What responsibilities did they handle independently?"
            ]
        elif "colleague" in reference_type.lower():
            role_questions = [
                "How did they collaborate with the team?",
                "What made them a valuable team member?"
            ]

        all_questions = self.base_questions + role_questions

        # Copy-paste template
        template = f"""Hey [Name],

I'm using Resumaker to build my resume for {target_role} positions. As part of the process, I'm gathering input from people I've worked with to make sure my resume accurately reflects my experience.

Would you mind answering a few quick questions about working with me? It should only take 5 minutes.

You can either:
1. Click this link: {share_url}
2. Or just reply to this message with your thoughts on these questions:

{chr(10).join([f'{i+1}. {q}' for i, q in enumerate(all_questions)])}

Thanks so much!
"""

        return {
            "share_token": share_token,
            "share_url": share_url,
            "copy_paste_template": template,
            "questions": all_questions,
            "expires_at": (datetime.now() + timedelta(days=30)).isoformat()
        }

    async def parse_reference_response(self, response_text: str) -> dict:
        """Parse reference response and extract structured data"""

        # Use Claude to parse the response
        from anthropic import Anthropic
        client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

        prompt = f"""Parse this reference response and extract resume-relevant information.

Reference response:
{response_text}

Return JSON:
{{
  "accomplishments": ["list of specific accomplishments mentioned"],
  "skills": ["list of skills mentioned"],
  "quotes": ["memorable quotes that could be used"],
  "stories": ["specific examples or anecdotes"],
  "strengths": ["key strengths identified"]
}}"""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        response = message.content[0].text
        if response.startswith('```json'):
            response = response.split('```json')[1].split('```')[0].strip()

        import json
        return json.loads(response)

# Singleton
reference_service = ReferenceService()
