"""Conversation Service - AI-powered resume data collection"""

from anthropic import Anthropic
import os
from dotenv import load_dotenv
import json

load_dotenv()

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# Question bank (40 questions across 7 categories)
QUESTION_BANK = {
    "professional_identity": [
        "What's your current or most recent job title and what does it really mean in plain terms?",
        "If you had to explain your job to a 10-year-old, what would you say you do?",
        "What industry or field do you work in?",
        "What are you known for professionally?",
        "What's the one thing people come to you for at work?"
    ],
    "accomplishments": [
        "Tell me about a time you made something better, faster, or cheaper at work.",
        "What's your proudest professional accomplishment?",
        "Have you ever saved your company money? How much and how?",
        "What's the biggest project you've led or been part of?",
        "Tell me about a time you went above and beyond expectations.",
        "Have you won any awards or recognition? What for?",
        "What's something you built or created that you're proud of?"
    ],
    "skills_expertise": [
        "What software, tools, or systems do you use daily?",
        "What technical skills do you have that others might not?",
        "What languages do you speak (programming or human)?",
        "What can you do that would be hard to replace?",
        "If someone shadowed you for a day, what would they see you doing?",
        "What do you know more about than most people?"
    ],
    "growth_challenges": [
        "Tell me about a time you failed and what you learned.",
        "What was the hardest problem you've solved at work?",
        "How have you grown professionally in the last 2 years?",
        "What skill did you have to learn on the job?",
        "What feedback have you gotten that changed how you work?"
    ],
    "experience_details": [
        "Walk me through a typical day or week at your current/recent job.",
        "Who did you report to and who reported to you?",
        "What was the team size and structure?",
        "What were your actual responsibilities vs what the job description said?",
        "How did you measure success in this role?",
        "What would your manager say about your performance?",
        "Why did you leave (or why are you looking to leave)?"
    ],
    "metrics_data": [
        "How many people, clients, or users did you support/serve?",
        "What was your budget or the value of what you managed?",
        "What were the quantifiable results of your work?",
        "How did you improve efficiency or productivity? By how much?",
        "What numbers define your impact?"
    ],
    "stories_anecdotes": [
        "Tell me about a time you had to influence someone without authority.",
        "Describe a situation where you had to make a tough decision.",
        "What's a story your colleagues would tell about you?",
        "Tell me about a time you collaborated across teams or departments.",
        "What's an example of you showing leadership (even if you weren't the manager)?"
    ]
}

class ConversationService:
    def __init__(self):
        self.client = Anthropic(api_key=CLAUDE_API_KEY)

    async def start_conversation(self, user_id: str) -> dict:
        """Start a new conversation session"""
        # Select first question
        first_question = QUESTION_BANK["professional_identity"][0]

        return {
            "question": first_question,
            "category": "professional_identity",
            "question_index": 0,
            "total_questions": 40
        }

    async def continue_conversation(self, conversation_history: list, user_response: str) -> dict:
        """Continue the conversation based on user's response"""

        # Build conversation context
        context = "\n\n".join([
            f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
            for msg in conversation_history
        ])

        # Ask Claude to extract knowledge and decide next question
        prompt = f"""You are helping someone build their resume through conversation.

Conversation so far:
{context}

User's latest response:
{user_response}

Your tasks:
1. Extract any resume-relevant information from this response
2. Decide what to ask next to gather more useful information

Available question categories and sample questions:
{json.dumps(QUESTION_BANK, indent=2)}

Return a JSON object:
{{
  "extracted_knowledge": {{
    "type": "accomplishment|skill|experience|story|metric|etc",
    "title": "brief title",
    "content": {{
      "description": "full extracted info",
      "metrics": [],
      "skills": [],
      "timeframe": ""
    }}
  }},
  "next_question": "the next question to ask",
  "reasoning": "why this question makes sense",
  "conversation_progress": "percentage complete (0-100)"
}}"""

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text

        # Clean JSON
        if response_text.startswith('```json'):
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif response_text.startswith('```'):
            response_text = response_text.split('```')[1].split('```')[0].strip()

        return json.loads(response_text)

# Singleton
conversation_service = ConversationService()
