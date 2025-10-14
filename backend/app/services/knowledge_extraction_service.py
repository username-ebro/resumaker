"""Knowledge Extraction Service - Turns conversations/resumes into structured facts"""

import anthropic
import os
from dotenv import load_dotenv
from datetime import datetime
import json
import re
import time
from typing import Dict, List, Optional

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

class KnowledgeExtractionService:
    """Extracts structured knowledge entities from unstructured text"""

    def __init__(self):
        self.client = client
        self.extracted_cache = {}  # Track extracted items to avoid duplicates

    async def extract_from_conversation(self, conversation_history: list, user_id: str, source_reference: str = None) -> dict:
        """
        Extract structured facts from conversation history

        Args:
            conversation_history: List of {role, content} messages
            user_id: UUID of user
            source_reference: ID of conversation for tracking

        Returns:
            Dict with entities and relationships
        """

        # Build conversation text
        conversation_text = self._format_conversation(conversation_history)

        # Extract using Claude
        extraction_prompt = self._build_extraction_prompt(conversation_text, "conversation")

        # Retry logic with exponential backoff
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=4000,
                    temperature=0.0,  # Deterministic extraction
                    messages=[{
                        "role": "user",
                        "content": extraction_prompt
                    }]
                )

                # Parse JSON response
                extracted_data = self._parse_and_validate_json(response.content[0].text)

                if not extracted_data:
                    raise ValueError("Invalid JSON response from extraction")

                # Validate confidence scores
                entities = extracted_data.get("entities", [])
                validated_entities = self._validate_entities(entities)

                # Deduplicate entities
                deduplicated_entities = self._deduplicate_entities(validated_entities, user_id)

                # Add metadata
                enriched_entities = self._enrich_entities(
                    deduplicated_entities,
                    user_id=user_id,
                    source="conversation",
                    source_reference=source_reference
                )

                relationships = extracted_data.get("relationships", [])

                return {
                    "success": True,
                    "entities": enriched_entities,
                    "relationships": relationships,
                    "total_extracted": len(enriched_entities),
                    "duplicates_removed": len(validated_entities) - len(deduplicated_entities)
                }

            except json.JSONDecodeError as e:
                print(f"JSON parsing error (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                return {
                    "success": False,
                    "error": f"JSON parsing failed after {max_retries} attempts",
                    "entities": [],
                    "relationships": []
                }

            except Exception as e:
                print(f"Extraction error (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                return {
                    "success": False,
                    "error": str(e),
                    "entities": [],
                    "relationships": []
                }

    async def extract_from_resume(self, resume_text: str, user_id: str, source_reference: str = None) -> dict:
        """
        Extract structured facts from resume text

        Args:
            resume_text: Raw text extracted from resume
            user_id: UUID of user
            source_reference: File ID for tracking

        Returns:
            Dict with entities and relationships
        """

        extraction_prompt = self._build_extraction_prompt(resume_text, "resume")

        # Retry logic with exponential backoff
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=4000,
                    temperature=0.0,  # Deterministic extraction
                    messages=[{
                        "role": "user",
                        "content": extraction_prompt
                    }]
                )

                # Parse JSON response
                extracted_data = self._parse_and_validate_json(response.content[0].text)

                if not extracted_data:
                    raise ValueError("Invalid JSON response from extraction")

                # Validate confidence scores
                entities = extracted_data.get("entities", [])
                validated_entities = self._validate_entities(entities)

                # Deduplicate entities
                deduplicated_entities = self._deduplicate_entities(validated_entities, user_id)

                # Add metadata
                enriched_entities = self._enrich_entities(
                    deduplicated_entities,
                    user_id=user_id,
                    source="resume_upload",
                    source_reference=source_reference
                )

                relationships = extracted_data.get("relationships", [])

                return {
                    "success": True,
                    "entities": enriched_entities,
                    "relationships": relationships,
                    "total_extracted": len(enriched_entities),
                    "duplicates_removed": len(validated_entities) - len(deduplicated_entities)
                }

            except json.JSONDecodeError as e:
                print(f"JSON parsing error (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                return {
                    "success": False,
                    "error": f"JSON parsing failed after {max_retries} attempts",
                    "entities": [],
                    "relationships": []
                }

            except Exception as e:
                print(f"Extraction error (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                return {
                    "success": False,
                    "error": str(e),
                    "entities": [],
                    "relationships": []
                }

    def _format_conversation(self, conversation_history: list) -> str:
        """Format conversation messages into readable text"""
        formatted = []
        for msg in conversation_history:
            role = msg.get("role", "user").upper()
            content = msg.get("content", "")
            formatted.append(f"{role}: {content}")
        return "\n\n".join(formatted)

    def _build_extraction_prompt(self, input_text: str, source_type: str) -> str:
        """Build the extraction prompt for Claude with few-shot examples"""

        # Few-shot examples based on source type
        examples = self._get_few_shot_examples(source_type)

        return f"""You are a fact extraction engine for a resume builder. Extract discrete, verifiable facts from the user's {source_type}.

{examples}

NOW EXTRACT FROM THIS INPUT:
{input_text}

Extract facts in this EXACT JSON structure:
{{
  "entities": [
    {{
      "entity_type": "job",
      "title": "Job Title",
      "description": "Full description of role",
      "start_date": "YYYY-MM-DD or null",
      "end_date": "YYYY-MM-DD or null",
      "is_current": true/false,
      "confidence_score": 0.00-1.00,
      "structured_data": {{
        "company": "Company Name",
        "location": "City, State or null",
        "industry": "Industry or null"
      }},
      "details": [
        {{
          "entity_type": "job_detail",
          "title": "Brief summary of responsibility",
          "description": "Full description of what they did",
          "confidence_score": 0.00-1.00,
          "structured_data": {{
            "metrics": "30 teachers or null",
            "technologies": ["Python", "Django"] or null,
            "impact": "Improved X by Y%" or null,
            "team_size": "5 people" or null
          }}

          NOTE: job_detail entities NEVER have start_date/end_date fields - they inherit from parent job
        }}
      ]
    }},
    {{
      "entity_type": "skill",
      "title": "Skill Name",
      "description": "Context for how they use this skill",
      "confidence_score": 0.00-1.00,
      "structured_data": {{
        "skill_name": "Python",
        "skill_category": "technical_skill|soft_skill|tool|language|certification",
        "proficiency_level": "beginner|intermediate|advanced|expert or null",
        "years_experience": 5 or null,
        "last_used": "YYYY-MM-DD or null",
        "context": "universal|job_specific or null"
      }}

      NOTE: Skills listed in a general "SKILLS" section (not under a specific job) are "universal"
            Skills demonstrated in a specific job context should be "job_specific"
    }},
    {{
      "entity_type": "project",
      "title": "Project Name",
      "description": "What the project was about",
      "start_date": "YYYY-MM-DD or null",
      "end_date": "YYYY-MM-DD or null",
      "confidence_score": 0.00-1.00,
      "structured_data": {{
        "project_name": "Name",
        "technologies": ["React", "Node.js"],
        "role": "Lead Developer or null",
        "team_size": "3 people or null",
        "url": "https://... or null"
      }}
    }},
    {{
      "entity_type": "education",
      "title": "Degree/Certification Name",
      "description": "Details about education",
      "start_date": "YYYY-MM-DD or null",
      "end_date": "YYYY-MM-DD or null",
      "confidence_score": 0.00-1.00,
      "structured_data": {{
        "institution": "University Name",
        "degree_or_cert": "Bachelor's in Computer Science",
        "field_of_study": "Computer Science or null",
        "gpa": "3.8 or null"
      }}
    }},
    {{
      "entity_type": "achievement",
      "title": "Achievement Title",
      "description": "Full description",
      "confidence_score": 0.00-1.00,
      "structured_data": {{
        "date": "YYYY-MM-DD or null",
        "organization": "Who gave the award or null",
        "metrics": "Increased sales by 30% or null"
      }}
    }}
  ],
  "relationships": [
    {{
      "from_entity_index": 0,
      "to_entity_index": 1,
      "relationship_type": "used_in|requires|achieved_at|related_to|supports",
      "strength": 0.00-1.00,
      "description": "Why these are connected"
    }}
  ]
}}

EXTRACTION RULES:
1. Only extract facts that are EXPLICITLY stated or STRONGLY implied
2. Use confidence_score to indicate uncertainty (vague = 0.60, specific = 0.95)
3. Break complex statements into atomic facts (one fact = one entity)
4. Preserve exact dates, numbers, company names, and proper nouns IN FULL - NEVER TRUNCATE
5. **CRITICAL DATE FORMAT RULES:**
   - Full date (day/month/year): "YYYY-MM-DD" (e.g., "2023-08-15")
   - Month and year ONLY: "YYYY-MM" (e.g., "2016-08" for August 2016)
   - Year only: "YYYY" (e.g., "2020")
   - Unknown/not mentioned: null
   - **EXAMPLES:**
     * "August 2016" → "2016-08"
     * "08/2016" → "2016-08"
     * "Fall 2020" → "2020-09"
     * "January 2023" → "2023-01"
     * "2019 to present" → start_date: "2019", end_date: null, is_current: true
6. **CRITICAL NAME PRESERVATION:**
   - Extract FULL names, NEVER abbreviate or truncate
   - "Livingston Collegiate Academy" → USE FULL NAME (NOT "Living Academy")
   - "Massachusetts Institute of Technology" → USE FULL NAME (NOT "MIT")
7. **CRITICAL - DATE INHERITANCE FOR JOB_DETAILS:**
   - job_detail entities inherit parent job's start_date and end_date AUTOMATICALLY
   - DO NOT include start_date/end_date fields in job_detail objects
   - Example: "Consultant (08/22 - Present)" with 3 bullet points → All 3 inherit 08/22 - Present
   - This ensures chronological accuracy: accomplishments are tied to specific time periods
8. For job_detail entities: Each should be a distinct responsibility or achievement
9. Link related entities via relationships array (use array indexes)
10. If ambiguous, mark confidence < 0.70
11. **CRITICAL - UNIVERSAL VS JOB-SPECIFIC SKILLS:**
   - Skills in a standalone "SKILLS" section (bottom of resume) → context: "universal", NO start_date/end_date
   - Skills demonstrated within a job description → context: "job_specific", inherit job dates
   - Example: "Python, JavaScript, SQL" at bottom of resume → universal skills
   - Example: "Used Python to build..." in Consultant job → job_specific skill with 08/22 - Present dates
12. For skills: Only extract if explicitly mentioned or clearly demonstrated
13. Nested entities (job -> job_detail): Put details inside "details" array, NOT as separate top-level entities

RETURN ONLY VALID JSON. No markdown, no code blocks, no explanation.
"""

    def _enrich_entities(self, entities: list, user_id: str, source: str, source_reference: str = None) -> list:
        """Add metadata to extracted entities"""

        enriched = []

        for entity in entities:
            # Add system metadata
            entity["user_id"] = user_id
            entity["source"] = source
            entity["source_reference"] = source_reference
            entity["is_confirmed"] = False  # Requires user confirmation
            entity["created_at"] = datetime.now().isoformat()

            # Process nested details (for jobs)
            if "details" in entity:
                for detail in entity["details"]:
                    detail["user_id"] = user_id
                    detail["source"] = source
                    detail["source_reference"] = source_reference
                    detail["is_confirmed"] = False
                    detail["created_at"] = datetime.now().isoformat()

                    # 🎯 CRITICAL: Inherit parent job's dates for chronological accuracy
                    # All bullet points under "Consultant (08/22 - Present)" must be dated 08/22 - Present
                    detail["start_date"] = entity.get("start_date")
                    detail["end_date"] = entity.get("end_date")
                    detail["is_current"] = entity.get("is_current", False)

            enriched.append(entity)

        return enriched

    async def update_entity(self, entity_id: str, updates: dict) -> dict:
        """
        Update an extracted entity (used when user edits before confirming)
        """
        # This will be handled by knowledge_graph_service
        pass

    def categorize_entity_type(self, entity_data: dict) -> str:
        """
        Determine entity type from content
        (Fallback if AI doesn't categorize correctly)
        """

        # Simple heuristics
        if "company" in entity_data.get("structured_data", {}):
            return "job"
        elif "skill_name" in entity_data.get("structured_data", {}):
            return "skill"
        elif "project_name" in entity_data.get("structured_data", {}):
            return "project"
        elif "institution" in entity_data.get("structured_data", {}):
            return "education"
        else:
            return "personal"

    def _parse_and_validate_json(self, text: str) -> Optional[dict]:
        """Parse JSON and validate structure"""
        try:
            # Remove markdown code blocks if present
            text = re.sub(r'^```json\s*', '', text, flags=re.MULTILINE)
            text = re.sub(r'^```\s*$', '', text, flags=re.MULTILINE)
            text = text.strip()

            # Parse JSON
            data = json.loads(text)

            # Validate required keys
            if "entities" not in data:
                print("Warning: No 'entities' key in extracted data")
                data["entities"] = []

            if "relationships" not in data:
                data["relationships"] = []

            return data

        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
            print(f"Text snippet: {text[:200]}")
            return None

    def _validate_entities(self, entities: List[dict]) -> List[dict]:
        """Validate and fix entity data"""
        validated = []

        for entity in entities:
            # Ensure required fields exist
            if not entity.get("entity_type"):
                print(f"Skipping entity without type: {entity.get('title', 'Unknown')}")
                continue

            if not entity.get("title"):
                print(f"Skipping entity without title: {entity}")
                continue

            # Validate confidence score
            confidence = entity.get("confidence_score", 0.80)
            try:
                confidence = float(confidence)
                if confidence < 0.0 or confidence > 1.0:
                    print(f"Invalid confidence score {confidence}, setting to 0.80")
                    confidence = 0.80
            except (ValueError, TypeError):
                print(f"Invalid confidence score format, setting to 0.80")
                confidence = 0.80

            entity["confidence_score"] = confidence

            # Validate nested details
            if "details" in entity:
                validated_details = []
                for detail in entity.get("details", []):
                    if detail.get("title") and detail.get("entity_type"):
                        # Validate detail confidence
                        detail_conf = detail.get("confidence_score", 0.80)
                        try:
                            detail_conf = float(detail_conf)
                            if detail_conf < 0.0 or detail_conf > 1.0:
                                detail_conf = 0.80
                        except (ValueError, TypeError):
                            detail_conf = 0.80
                        detail["confidence_score"] = detail_conf
                        validated_details.append(detail)

                entity["details"] = validated_details

            validated.append(entity)

        return validated

    def _deduplicate_entities(self, entities: List[dict], user_id: str) -> List[dict]:
        """Remove duplicate entities based on title and type"""
        seen = set()
        deduplicated = []

        # Build cache key for user session
        cache_key = f"{user_id}_session"
        if cache_key not in self.extracted_cache:
            self.extracted_cache[cache_key] = set()

        for entity in entities:
            # Create unique key for entity
            entity_type = entity.get("entity_type", "")
            title = entity.get("title", "").strip().lower()
            unique_key = f"{entity_type}:{title}"

            # Check if already extracted in this session
            if unique_key in self.extracted_cache[cache_key]:
                print(f"Duplicate detected (session cache): {title}")
                continue

            # Check if duplicate in current batch
            if unique_key in seen:
                print(f"Duplicate detected (current batch): {title}")
                continue

            seen.add(unique_key)
            self.extracted_cache[cache_key].add(unique_key)
            deduplicated.append(entity)

        return deduplicated

    def _get_few_shot_examples(self, source_type: str) -> str:
        """Get few-shot examples based on source type"""

        if source_type == "conversation":
            return """EXAMPLE INPUT (Conversation):
USER: I worked at Google for 3 years as a software engineer
AI: What did you work on there?
USER: I built the search autocomplete feature and improved response time by 40%

EXAMPLE OUTPUT:
{
  "entities": [
    {
      "entity_type": "job",
      "title": "Software Engineer at Google",
      "description": "Worked as a software engineer at Google for 3 years",
      "start_date": null,
      "end_date": null,
      "is_current": false,
      "confidence_score": 0.95,
      "structured_data": {
        "company": "Google",
        "location": null,
        "industry": "Technology"
      },
      "details": [
        {
          "entity_type": "job_detail",
          "title": "Built search autocomplete feature",
          "description": "Built the search autocomplete feature and improved response time by 40%",
          "confidence_score": 0.95,
          "structured_data": {
            "metrics": "40% improvement",
            "technologies": null,
            "impact": "Improved response time by 40%",
            "team_size": null
          }
        }
      ]
    },
    {
      "entity_type": "skill",
      "title": "Software Engineering",
      "description": "Demonstrated through work at Google building search features",
      "confidence_score": 0.90,
      "structured_data": {
        "skill_name": "Software Engineering",
        "skill_category": "technical_skill",
        "proficiency_level": "advanced",
        "years_experience": 3,
        "last_used": null
      }
    }
  ],
  "relationships": [
    {
      "from_entity_index": 1,
      "to_entity_index": 0,
      "relationship_type": "used_in",
      "strength": 0.90,
      "description": "Software engineering skills used in Google job"
    }
  ]
}"""
        else:  # resume
            return """EXAMPLE INPUT (Resume):
John Doe
Senior Product Manager | NYC
john@email.com | linkedin.com/in/johndoe

EXPERIENCE
Product Manager - Acme Corp (2020-2023)
- Led product development for mobile app with 500K users
- Increased user retention by 35% through data-driven UX improvements
- Managed cross-functional team of 8 engineers and designers

SKILLS
Product Management, Agile, SQL, Figma

EXAMPLE OUTPUT:
{
  "entities": [
    {
      "entity_type": "personal",
      "title": "John Doe",
      "description": "Senior Product Manager based in NYC",
      "confidence_score": 1.0,
      "structured_data": {
        "name": "John Doe",
        "current_title": "Senior Product Manager",
        "location": "NYC",
        "email": "john@email.com",
        "linkedin": "linkedin.com/in/johndoe"
      }
    },
    {
      "entity_type": "job",
      "title": "Product Manager at Acme Corp",
      "description": "Led product development for mobile app with 500K users",
      "start_date": "2020",
      "end_date": "2023",
      "is_current": false,
      "confidence_score": 1.0,
      "structured_data": {
        "company": "Acme Corp",
        "location": null,
        "industry": null
      },
      "details": [
        {
          "entity_type": "job_detail",
          "title": "Led mobile app product development",
          "description": "Led product development for mobile app with 500K users",
          "confidence_score": 1.0,
          "structured_data": {
            "metrics": "500K users",
            "technologies": null,
            "impact": null,
            "team_size": null
          }
        },
        {
          "entity_type": "job_detail",
          "title": "Increased user retention through UX improvements",
          "description": "Increased user retention by 35% through data-driven UX improvements",
          "confidence_score": 1.0,
          "structured_data": {
            "metrics": "35% increase",
            "technologies": null,
            "impact": "Increased user retention by 35%",
            "team_size": null
          }
        },
        {
          "entity_type": "job_detail",
          "title": "Managed cross-functional team",
          "description": "Managed cross-functional team of 8 engineers and designers",
          "confidence_score": 1.0,
          "structured_data": {
            "metrics": null,
            "technologies": null,
            "impact": null,
            "team_size": "8 people"
          }
        }
      ]
    },
    {
      "entity_type": "skill",
      "title": "Product Management",
      "description": "Core skill demonstrated through product management role",
      "confidence_score": 1.0,
      "structured_data": {
        "skill_name": "Product Management",
        "skill_category": "soft_skill",
        "proficiency_level": "expert",
        "years_experience": 3,
        "last_used": "2023"
      }
    },
    {
      "entity_type": "skill",
      "title": "Agile",
      "description": "Listed as a skill",
      "confidence_score": 0.85,
      "structured_data": {
        "skill_name": "Agile",
        "skill_category": "soft_skill",
        "proficiency_level": null,
        "years_experience": null,
        "last_used": null
      }
    },
    {
      "entity_type": "skill",
      "title": "SQL",
      "description": "Listed as a skill",
      "confidence_score": 0.85,
      "structured_data": {
        "skill_name": "SQL",
        "skill_category": "technical_skill",
        "proficiency_level": null,
        "years_experience": null,
        "last_used": null
      }
    },
    {
      "entity_type": "skill",
      "title": "Figma",
      "description": "Listed as a skill",
      "confidence_score": 0.85,
      "structured_data": {
        "skill_name": "Figma",
        "skill_category": "tool",
        "proficiency_level": null,
        "years_experience": null,
        "last_used": null
      }
    }
  ],
  "relationships": [
    {
      "from_entity_index": 2,
      "to_entity_index": 1,
      "relationship_type": "used_in",
      "strength": 0.95,
      "description": "Product Management skills used in Acme Corp role"
    },
    {
      "from_entity_index": 3,
      "to_entity_index": 1,
      "relationship_type": "used_in",
      "strength": 0.80,
      "description": "Agile methodology likely used in product management role"
    }
  ]
}"""


# Singleton instance
knowledge_extraction_service = KnowledgeExtractionService()
