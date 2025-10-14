"""
Resume Generator Service
Compiles knowledge base entries into ATS-optimized resumes
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import anthropic
import os
from ..database import get_supabase
from ..utils.user_utils import ensure_user_profile

class ResumeGenerator:
    def __init__(self):
        self.claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.supabase = get_supabase()

        # Load ATS guide
        ats_guide_path = os.path.join(os.path.dirname(__file__), "../../data/ATS_Resume_Optimization_Guide_2025.md")
        with open(ats_guide_path, 'r') as f:
            self.ats_guide = f.read()

    async def generate_resume(
        self,
        user_id: str,
        job_description: Optional[str] = None,
        target_role: Optional[str] = None,
        user_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a complete resume from user's knowledge base

        Args:
            user_id: UUID of the user
            job_description: Optional job description to tailor resume
            target_role: Optional target role for optimization
            user_prompt: Optional free-form prompt for generic resume
                        (e.g., "applying for concession stand position")

        Returns:
            Dictionary with resume structure and content
        """
        # 1. Fetch all knowledge base entries
        knowledge_base = await self._fetch_knowledge_base(user_id)

        # 2. Fetch user profile
        profile = await self._fetch_user_profile(user_id)

        # 3. If user_prompt provided, filter relevant facts FIRST
        if user_prompt and not job_description:
            # Generic mode: Select relevant facts based on prompt
            knowledge_base = await self.select_relevant_facts(user_prompt, knowledge_base)

        # 4. Organize knowledge by type
        organized_knowledge = self._organize_knowledge(knowledge_base)

        # 5. Extract keywords from job description if provided
        target_keywords = []
        if job_description:
            target_keywords = await self._extract_keywords(job_description)
        elif user_prompt:
            # Extract keywords from user prompt for generic mode
            target_keywords = await self._extract_keywords_from_prompt(user_prompt)

        # 6. Generate professional summary
        summary = await self._generate_summary(
            profile=profile,
            knowledge=organized_knowledge,
            target_role=target_role or user_prompt,
            keywords=target_keywords
        )

        # 7. Generate work experience section
        experience = await self._generate_experience(
            knowledge=organized_knowledge,
            keywords=target_keywords
        )

        # 8. Generate skills section
        skills = await self._generate_skills(
            knowledge=organized_knowledge,
            keywords=target_keywords
        )

        # 9. Generate education section
        education = self._generate_education(organized_knowledge)

        # 10. Generate certifications section
        certifications = self._generate_certifications(organized_knowledge)

        # 11. Assemble complete resume
        resume_structure = {
            "contact_info": {
                "name": profile.get("full_name", ""),
                "email": profile.get("email", ""),
                "phone": profile.get("phone", ""),
                "location": profile.get("location", ""),
                "linkedin": profile.get("linkedin_url", ""),
                "portfolio": profile.get("portfolio_url", "")
            },
            "summary": summary,
            "experience": experience,
            "skills": skills,
            "education": education,
            "certifications": certifications,
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "knowledge_base_entries_used": len(knowledge_base),
                "target_role": target_role or user_prompt,
                "job_targeted": bool(job_description),
                "generic_mode": bool(user_prompt and not job_description)
            }
        }

        return resume_structure

    async def select_relevant_facts(
        self,
        user_prompt: str,
        all_entities: List[Dict]
    ) -> List[Dict]:
        """
        Use Claude to select relevant facts based on user's prompt

        Example:
            Prompt: "applying for concession stand position"
            Picks: customer service skills, cash handling, NOT programming

        Args:
            user_prompt: User's description of what they're applying for
            all_entities: All knowledge base entries

        Returns:
            Filtered list of relevant entities
        """

        # Build summary of all facts
        facts_summary = []
        for idx, entity in enumerate(all_entities):
            fact_type = entity.get('knowledge_type', 'unknown')
            title = entity.get('title', 'Untitled')
            content_preview = str(entity.get('content', ''))[:100]

            facts_summary.append(f"{idx}. [{fact_type}] {title}: {content_preview}")

        facts_text = "\n".join(facts_summary[:100])  # Limit to 100 facts

        prompt = f"""A user is creating a resume for: "{user_prompt}"

Here are all their facts/experiences (ID, type, title):
{facts_text}

Select the MOST RELEVANT fact IDs (numbers) for this application.

Rules:
1. Select 10-20 most relevant facts
2. Prioritize facts that match the role/industry
3. Exclude obviously irrelevant facts
4. Include transferable skills

Examples:
- If applying for "concession stand": Include customer service, cash handling, fast-paced work
- If applying for "software engineer": Include programming, projects, technical skills
- If applying for "marketing": Include communication, social media, campaigns

Return ONLY a JSON array of fact IDs:
[0, 3, 5, 12, 15]

Return ONLY the JSON array, no explanation."""

        try:
            message = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text.strip()

            # Parse JSON array
            import json
            selected_ids = json.loads(response_text)

            # Filter entities
            relevant_entities = [
                all_entities[idx]
                for idx in selected_ids
                if idx < len(all_entities)
            ]

            print(f"Selected {len(relevant_entities)} relevant facts from {len(all_entities)} total")

            return relevant_entities

        except Exception as e:
            print(f"Error selecting relevant facts: {str(e)}")
            # Fallback: return all entities
            return all_entities

    async def _extract_keywords_from_prompt(self, user_prompt: str) -> List[str]:
        """
        Extract keywords from user's free-form prompt

        Args:
            user_prompt: e.g., "applying for concession stand position"

        Returns:
            List of relevant keywords
        """

        prompt_text = f"""Extract 5-10 key skills/keywords relevant to this application:

"{user_prompt}"

Return ONLY a comma-separated list of keywords.

Examples:
- "applying for concession stand" -> customer service, cash handling, food service, fast-paced, teamwork
- "software engineering internship" -> programming, coding, algorithms, teamwork, problem-solving
- "marketing coordinator role" -> marketing, social media, content creation, analytics, communication

Prompt: {user_prompt}
Keywords:"""

        try:
            message = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=150,
                messages=[{"role": "user", "content": prompt_text}]
            )

            keywords_text = message.content[0].text.strip()
            keywords = [k.strip() for k in keywords_text.split(',')]

            return keywords

        except Exception as e:
            print(f"Error extracting keywords from prompt: {str(e)}")
            return []

    async def _fetch_knowledge_base(self, user_id: str) -> List[Dict]:
        """Fetch all confirmed knowledge entities for user"""
        # FIXED: Was querying user_knowledge_base (empty), now queries knowledge_entities (has data)
        result = self.supabase.table("knowledge_entities")\
            .select("*")\
            .eq("user_id", user_id)\
            .eq("is_confirmed", True)\
            .order("created_at", desc=True)\
            .execute()

        # Transform knowledge_entities schema to match expected format
        transformed_data = []
        for entity in result.data:
            # Map entity_type to knowledge_type
            knowledge_type = self._map_entity_type_to_knowledge_type(entity.get('entity_type', 'experience'))

            transformed_data.append({
                'id': entity['id'],
                'user_id': entity['user_id'],
                'parent_id': entity.get('parent_id'),  # 🎯 Preserve parent-child relationships
                'entity_type': entity.get('entity_type'),  # Keep original type for reference
                'title': entity.get('title', ''),
                'content': entity.get('structured_data', {}) or {'description': entity.get('description', '')},
                'knowledge_type': knowledge_type,
                'tags': entity.get('tags', []),
                'date_range': self._build_date_range(entity.get('start_date'), entity.get('end_date')),
                'created_at': entity.get('created_at', '')
            })

        return transformed_data

    def _map_entity_type_to_knowledge_type(self, entity_type: str) -> str:
        """Map knowledge_entities.entity_type to knowledge_type"""
        mapping = {
            'job': 'experience',
            'work_experience': 'experience',
            'job_experience': 'experience',
            'job_detail': 'accomplishment',
            'education': 'education',
            'skill': 'skill',
            'achievement': 'accomplishment',
            'accomplishment': 'accomplishment',
            'certification': 'certification',
            'project': 'project',
            'metric': 'metric',
            'story': 'story'
        }
        return mapping.get(entity_type.lower(), 'experience')

    def _build_date_range(self, start_date, end_date) -> Optional[str]:
        """Build PostgreSQL date range format from start/end dates"""
        if not start_date and not end_date:
            return None

        start = start_date or '1900-01-01'
        end = end_date or '9999-12-31'
        return f"[{start},{end})"

    async def _fetch_user_profile(self, user_id: str) -> Dict:
        """Fetch user profile information, creating default if missing"""
        return await ensure_user_profile(user_id)

    def _organize_knowledge(self, knowledge_base: List[Dict]) -> Dict[str, List[Dict]]:
        """Organize knowledge entries by type"""
        organized = {
            'accomplishments': [],
            'skills': [],
            'experiences': [],
            'stories': [],
            'metrics': [],
            'certifications': [],
            'education': [],
            'projects': []
        }

        for entry in knowledge_base:
            k_type = entry['knowledge_type']
            if k_type == 'accomplishment':
                organized['accomplishments'].append(entry)
            elif k_type == 'skill':
                organized['skills'].append(entry)
            elif k_type == 'experience':
                organized['experiences'].append(entry)
            elif k_type == 'story':
                organized['stories'].append(entry)
            elif k_type == 'metric':
                organized['metrics'].append(entry)
            elif k_type == 'certification':
                organized['certifications'].append(entry)
            elif k_type == 'education':
                organized['education'].append(entry)
            elif k_type == 'project':
                organized['projects'].append(entry)

        return organized

    async def _extract_keywords(self, job_description: str) -> List[str]:
        """Extract key terms from job description using Claude"""
        prompt = f"""Extract the 15-20 most important keywords and key phrases from this job description.
Focus on:
1. Required skills (technical and soft)
2. Tools and technologies
3. Job title variations
4. Industry buzzwords
5. Certifications mentioned
6. Key responsibilities

Job Description:
{job_description}

Return ONLY a comma-separated list of keywords, no explanations."""

        message = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        keywords_text = message.content[0].text
        keywords = [k.strip() for k in keywords_text.split(',')]

        return keywords

    async def _generate_summary(
        self,
        profile: Dict,
        knowledge: Dict,
        target_role: Optional[str],
        keywords: List[str]
    ) -> str:
        """Generate professional summary using Claude with ATS optimization"""

        # Compile relevant accomplishments and experiences
        accomplishments_text = "\n".join([
            f"- {entry['title']}: {entry['content']}"
            for entry in knowledge['accomplishments'][:5]
        ])

        experiences_text = "\n".join([
            f"- {entry['title']}"
            for entry in knowledge['experiences'][:3]
        ])

        skills_text = ", ".join([
            entry['title']
            for entry in knowledge['skills'][:10]
        ])

        keywords_text = ", ".join(keywords) if keywords else "N/A"

        prompt = f"""You are an expert resume writer specializing in ATS optimization.

Create a compelling 3-4 sentence professional summary for this candidate.

CANDIDATE INFO:
- Target Role: {target_role or profile.get('target_role', 'N/A')}
- Years of Experience: {profile.get('years_of_experience', 'N/A')}
- Top Skills: {skills_text}

TOP ACCOMPLISHMENTS:
{accomplishments_text}

KEY EXPERIENCES:
{experiences_text}

TARGET KEYWORDS (incorporate naturally):
{keywords_text}

🚨 CRITICAL ANTI-HALLUCINATION RULES (MANDATORY):
1. ONLY use information EXPLICITLY provided above
2. NEVER invent years of experience, metrics, skills, or achievements
3. If a detail is "N/A" or missing, DO NOT fabricate it
4. If accomplishments list is empty, write a simple summary WITHOUT metrics
5. Every skill mentioned MUST appear in "Top Skills" or "Key Experiences" above
6. NO generic claims like "proven track record" without specific evidence
7. If you cannot write a fact-based summary, say "Insufficient information"

ATS OPTIMIZATION RULES:
1. Start with job title and years of experience (if provided)
2. Include 3-4 top skills/strengths that are LISTED above
3. Mention 1-2 quantifiable achievements (ONLY if listed in accomplishments)
4. Naturally integrate target keywords
5. Keep to 3-4 sentences maximum
6. Use strong action-oriented language
7. NO buzzwords or fluff - be specific

Return ONLY the summary text, no formatting or explanations."""

        message = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text.strip()

    async def _generate_experience(
        self,
        knowledge: Dict,
        keywords: List[str]
    ) -> List[Dict]:
        """Generate work experience section with ATS-optimized bullet points"""

        experiences = []

        # Group accomplishments and stories by experience/company
        for exp_entry in knowledge['experiences']:
            content = exp_entry['content']

            # Find related accomplishments and stories
            related_accomplishments = [
                a for a in knowledge['accomplishments']
                if self._is_related(a, exp_entry)
            ]

            related_stories = [
                s for s in knowledge['stories']
                if self._is_related(s, exp_entry)
            ]

            # Generate ATS-optimized bullet points
            bullets = await self._generate_bullets(
                experience=exp_entry,
                accomplishments=related_accomplishments,
                stories=related_stories,
                keywords=keywords
            )

            experience_item = {
                "title": content.get("job_title", exp_entry.get("title", "")),
                "company": content.get("company", ""),
                "location": content.get("location", ""),
                "start_date": self._format_date(exp_entry.get("date_range")),
                "end_date": self._format_date(exp_entry.get("date_range"), is_end=True),
                "bullets": bullets
            }

            experiences.append(experience_item)

        # Sort by date (most recent first)
        experiences.sort(
            key=lambda x: x.get("start_date", ""),
            reverse=True
        )

        return experiences

    async def _generate_bullets(
        self,
        experience: Dict,
        accomplishments: List[Dict],
        stories: List[Dict],
        keywords: List[str]
    ) -> List[str]:
        """Generate ATS-optimized bullet points for a position"""

        accomplishments_text = "\n".join([
            f"- {a['title']}: {a['content']}"
            for a in accomplishments[:10]
        ])

        stories_text = "\n".join([
            f"- {s['title']}: {s['content']}"
            for s in stories[:5]
        ])

        keywords_text = ", ".join(keywords[:15]) if keywords else "N/A"

        prompt = f"""You are an expert resume writer specializing in ATS optimization.

Create 5-7 ATS-optimized bullet points for this work experience.

POSITION: {experience.get('title', 'N/A')}
COMPANY: {experience['content'].get('company', 'N/A')}

ACCOMPLISHMENTS (SOURCE OF TRUTH):
{accomplishments_text}

RELEVANT STORIES/CONTEXT (SOURCE OF TRUTH):
{stories_text}

TARGET KEYWORDS (incorporate naturally):
{keywords_text}

🚨🚨 CRITICAL ANTI-HALLUCINATION RULES (VIOLATION = FAILURE) 🚨🚨:
1. **ONLY SOURCE MATERIAL ABOVE** - Every single fact, metric, technology, team size, or achievement MUST come from "ACCOMPLISHMENTS" or "STORIES" sections above
2. **ZERO FABRICATION** - If no metrics are provided, DO NOT invent percentages, dollar amounts, team sizes, or timeframes
3. **EMPTY SOURCE = GENERIC BULLETS** - If accomplishments/stories sections are empty, write simple responsibility-focused bullets WITHOUT specific metrics
4. **CITE YOUR SOURCE** - Each bullet must be traceable to a specific line in the SOURCE sections
5. **NO "ASSUMED" DETAILS** - Never add details like "increased by X%", "managed team of Y", "delivered in Z weeks" unless EXPLICITLY stated above
6. **QUALITY OVER QUANTITY** - Better to write 3 accurate bullets than 7 fabricated ones
7. **WHEN IN DOUBT, LEAVE IT OUT** - If you're uncertain about a detail, omit it

ATS OPTIMIZATION RULES:
1. Use formula: [Action Verb] + [What You Did] + [Quantifiable Result IF PROVIDED]
2. Start each bullet with a strong action verb (Led, Developed, Increased, Reduced, etc.)
3. Include metrics/numbers ONLY if they appear in SOURCE sections above
4. Naturally incorporate target keywords where truthful
5. Keep bullets concise (1-2 lines each)
6. Focus on impact and achievements when evidence exists
7. Use past tense for completed roles

Examples of GOOD bullets WITH evidence:
• Led cross-functional team of 12 using Agile methodology to deliver $2.5M enterprise software project 3 weeks ahead of schedule
• Implemented Salesforce CRM integration reducing sales cycle time by 30% and increasing conversion rate from 12% to 18%

Examples of GOOD bullets WITHOUT specific evidence:
• Collaborated with engineering team to deliver product features aligned with user needs
• Maintained codebase and implemented bug fixes to improve system stability
• Participated in agile development process and contributed to sprint planning

Return ONLY the bullet points (starting with •), no explanations or additional text."""

        message = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )

        bullets_text = message.content[0].text.strip()
        bullets = [line.strip() for line in bullets_text.split('\n') if line.strip().startswith('•')]

        return bullets

    async def _generate_skills(
        self,
        knowledge: Dict,
        keywords: List[str]
    ) -> Dict[str, List[str]]:
        """Generate categorized skills section"""

        all_skills = [entry['title'] for entry in knowledge['skills']]

        # Use Claude to categorize skills
        skills_text = ", ".join(all_skills)
        keywords_text = ", ".join(keywords) if keywords else ""

        prompt = f"""Categorize these skills into 3-4 groups. Prioritize skills that match the target keywords.

CANDIDATE'S SKILLS:
{skills_text}

TARGET KEYWORDS (prioritize these):
{keywords_text}

Create categories like:
- Technical Skills
- Tools & Technologies
- Methodologies
- Leadership & Management
- Languages (if applicable)

Return in this exact format:
Category Name: skill1, skill2, skill3
Category Name: skill1, skill2, skill3

Keep it concise - max 8-10 skills per category."""

        message = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse categorized skills
        categorized = {}
        lines = message.content[0].text.strip().split('\n')
        for line in lines:
            if ':' in line:
                category, skills = line.split(':', 1)
                skill_list = [s.strip() for s in skills.split(',')]
                categorized[category.strip()] = skill_list

        return categorized

    def _generate_education(self, knowledge: Dict) -> List[Dict]:
        """Generate education section from knowledge base"""
        education = []

        for entry in knowledge['education']:
            content = entry['content']
            education.append({
                "degree": content.get("degree", ""),
                "field": content.get("field", ""),
                "institution": content.get("institution", entry.get("title", "")),
                "graduation_date": content.get("graduation_date", ""),
                "gpa": content.get("gpa", ""),
                "honors": content.get("honors", [])
            })

        return education

    def _generate_certifications(self, knowledge: Dict) -> List[Dict]:
        """Generate certifications section from knowledge base"""
        certifications = []

        for entry in knowledge['certifications']:
            content = entry['content']
            certifications.append({
                "name": entry.get("title", ""),
                "issuer": content.get("issuer", ""),
                "date": content.get("date", ""),
                "credential_id": content.get("credential_id", ""),
                "url": content.get("url", "")
            })

        return certifications

    def _is_related(self, item: Dict, experience: Dict) -> bool:
        """
        Check if a knowledge item is related to an experience

        🎯 CHRONOLOGICAL ACCURACY:
        - job_details are linked via parent_id (strongest relationship)
        - Date range overlap means accomplishment happened during this job
        - This prevents "worked with 4 nonprofits" (Consultant) from appearing under Teacher
        """

        # 1. STRONGEST: Check parent-child relationship (job_detail -> job)
        if item.get('parent_id') == experience.get('id'):
            return True

        # 2. STRONG: Check if both have date ranges and they overlap
        item_dates = item.get('date_range')
        exp_dates = experience.get('date_range')

        if item_dates and exp_dates:
            try:
                # Parse date ranges: [start,end)
                item_start, item_end = item_dates.strip('[]()').split(',')
                exp_start, exp_end = exp_dates.strip('[]()').split(',')

                # Check for actual overlap (not just existence of dates)
                # Convert "9999-12-31" to "now" for current jobs
                item_end = None if item_end == '9999-12-31' else item_end
                exp_end = None if exp_end == '9999-12-31' else exp_end

                # If start date is within experience date range, they overlap
                if exp_start <= item_start and (exp_end is None or item_start <= exp_end):
                    return True

            except Exception as e:
                print(f"Date parsing error in _is_related: {e}")
                # Don't assume relationship on parse error
                pass

        # 3. MEDIUM: Check if tags overlap
        item_tags = set(item.get('tags', []))
        exp_tags = set(experience.get('tags', []))
        if item_tags & exp_tags:
            return True

        # 4. WEAK: Check if company mentioned in content
        exp_company = experience['content'].get('company', '')
        item_content_str = str(item.get('content', ''))
        if exp_company and exp_company.lower() in item_content_str.lower():
            return True

        return False

    def _format_date(self, date_range: Optional[str], is_end: bool = False) -> str:
        """Format date from PostgreSQL date range"""
        if not date_range:
            return ""

        # PostgreSQL date range format: [2020-01-01,2023-12-31)
        # Simple parsing - can be improved
        try:
            dates = date_range.strip('[]()').split(',')
            if is_end:
                return dates[1] if len(dates) > 1 else "Present"
            else:
                return dates[0]
        except:
            return ""

    async def generate_html_resume(self, resume_structure: Dict) -> str:
        """Convert resume structure to ATS-friendly HTML"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{resume_structure['contact_info']['name']} - Resume</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.15;
            margin: 0.5in;
            color: #000;
        }}
        h1 {{
            font-size: 18pt;
            margin: 0 0 5px 0;
            font-weight: bold;
        }}
        h2 {{
            font-size: 12pt;
            margin: 15px 0 5px 0;
            font-weight: bold;
            text-transform: uppercase;
            border-bottom: 1px solid #000;
        }}
        h3 {{
            font-size: 11pt;
            margin: 10px 0 3px 0;
            font-weight: bold;
        }}
        .contact-info {{
            text-align: center;
            margin-bottom: 15px;
        }}
        .contact-info p {{
            margin: 2px 0;
        }}
        .summary {{
            margin-bottom: 15px;
        }}
        .experience-item {{
            margin-bottom: 12px;
        }}
        .job-header {{
            margin-bottom: 3px;
        }}
        .job-title {{
            font-weight: bold;
        }}
        .company {{
            font-style: italic;
        }}
        ul {{
            margin: 5px 0;
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 3px;
        }}
        .skills-category {{
            margin-bottom: 8px;
        }}
        .category-name {{
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="contact-info">
        <h1>{resume_structure['contact_info']['name']}</h1>
        <p>{resume_structure['contact_info'].get('phone', '')} | {resume_structure['contact_info']['email']}</p>
        <p>{resume_structure['contact_info'].get('location', '')}</p>
        <p>{resume_structure['contact_info'].get('linkedin', '')} | {resume_structure['contact_info'].get('portfolio', '')}</p>
    </div>

    <h2>Professional Summary</h2>
    <div class="summary">
        <p>{resume_structure['summary']}</p>
    </div>

    <h2>Professional Experience</h2>
"""

        # Add experience items
        for exp in resume_structure['experience']:
            html += f"""    <div class="experience-item">
        <div class="job-header">
            <span class="job-title">{exp['title']}</span><br>
            <span class="company">{exp['company']}</span> | {exp.get('location', '')} | {exp.get('start_date', '')} - {exp.get('end_date', 'Present')}
        </div>
        <ul>
"""
            for bullet in exp['bullets']:
                html += f"            <li>{bullet.lstrip('•').strip()}</li>\n"

            html += "        </ul>\n    </div>\n"

        # Add skills
        html += "\n    <h2>Skills</h2>\n"
        for category, skills in resume_structure['skills'].items():
            skills_list = ", ".join(skills)
            html += f'    <div class="skills-category">\n'
            html += f'        <span class="category-name">{category}:</span> {skills_list}\n'
            html += '    </div>\n'

        # Add education
        if resume_structure['education']:
            html += "\n    <h2>Education</h2>\n"
            for edu in resume_structure['education']:
                html += f"""    <div>
        <h3>{edu.get('degree', '')} in {edu.get('field', '')}</h3>
        <p>{edu.get('institution', '')} | Graduated: {edu.get('graduation_date', '')}</p>
"""
                if edu.get('gpa'):
                    html += f"        <p>GPA: {edu['gpa']}</p>\n"
                html += "    </div>\n"

        # Add certifications
        if resume_structure['certifications']:
            html += "\n    <h2>Certifications</h2>\n    <ul>\n"
            for cert in resume_structure['certifications']:
                html += f"        <li>{cert['name']} | {cert.get('issuer', '')} | {cert.get('date', '')}</li>\n"
            html += "    </ul>\n"

        html += "</body>\n</html>"

        return html
