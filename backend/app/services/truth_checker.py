"""
Truth Verification Algorithm
Compares resume claims against knowledge base evidence
Conservative thresholds to maintain integrity
"""
from typing import List, Dict, Any, Tuple
from datetime import datetime
import anthropic
import os
from ..database import get_supabase

class TruthChecker:
    def __init__(self):
        self.claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.supabase = get_supabase()

    async def verify_resume(
        self,
        user_id: str,
        resume_structure: Dict[str, Any],
        resume_version_id: str
    ) -> Dict[str, Any]:
        """
        Verify all claims in a resume against knowledge base

        Args:
            user_id: UUID of the user
            resume_structure: The generated resume structure
            resume_version_id: UUID of the resume version being checked

        Returns:
            Dictionary with verification results and flags
        """
        # Fetch knowledge base
        knowledge_base = await self._fetch_knowledge_base(user_id)

        flags = []
        verification_report = {
            "total_checks": 0,
            "passed": 0,
            "flagged": 0,
            "severity_breakdown": {
                "low": 0,
                "medium": 0,
                "high": 0
            }
        }

        # 1. Verify professional summary claims
        summary_flags = await self._verify_summary(
            resume_structure['summary'],
            knowledge_base,
            resume_version_id
        )
        flags.extend(summary_flags)

        # 2. Verify each work experience bullet
        for exp_idx, experience in enumerate(resume_structure['experience']):
            exp_flags = await self._verify_experience(
                experience,
                knowledge_base,
                resume_version_id,
                exp_idx
            )
            flags.extend(exp_flags)

        # 3. Verify skills claims
        skills_flags = await self._verify_skills(
            resume_structure['skills'],
            knowledge_base,
            resume_version_id
        )
        flags.extend(skills_flags)

        # 4. Verify education claims
        edu_flags = await self._verify_education(
            resume_structure['education'],
            knowledge_base,
            resume_version_id
        )
        flags.extend(edu_flags)

        # 5. Verify certifications
        cert_flags = await self._verify_certifications(
            resume_structure['certifications'],
            knowledge_base,
            resume_version_id
        )
        flags.extend(cert_flags)

        # Calculate verification stats
        verification_report['total_checks'] = len(flags) if flags else 0
        verification_report['flagged'] = len([f for f in flags if f['severity'] in ['medium', 'high']])
        verification_report['passed'] = verification_report['total_checks'] - verification_report['flagged']

        for flag in flags:
            severity = flag['severity']
            verification_report['severity_breakdown'][severity] += 1

        # Store flags in database
        if flags:
            await self._store_flags(flags)

        return {
            "verification_report": verification_report,
            "flags": flags,
            "requires_review": verification_report['flagged'] > 0
        }

    async def _fetch_knowledge_base(self, user_id: str) -> List[Dict]:
        """Fetch all verified knowledge base entries"""
        result = self.supabase.table("user_knowledge_base")\
            .select("*")\
            .eq("user_id", user_id)\
            .execute()

        return result.data

    async def _verify_summary(
        self,
        summary: str,
        knowledge_base: List[Dict],
        resume_version_id: str
    ) -> List[Dict]:
        """Verify claims in professional summary"""

        # Extract accomplishments and experiences for context
        accomplishments = "\n".join([
            f"- {entry['title']}: {entry['content']}"
            for entry in knowledge_base
            if entry['knowledge_type'] == 'accomplishment'
        ])

        experiences = "\n".join([
            f"- {entry['title']}"
            for entry in knowledge_base
            if entry['knowledge_type'] == 'experience'
        ])

        metrics = "\n".join([
            f"- {entry['title']}: {entry['content']}"
            for entry in knowledge_base
            if entry['knowledge_type'] == 'metric'
        ])

        prompt = f"""You are a truth verification expert for resume accuracy.

Analyze this professional summary and identify any claims that are NOT fully supported by the evidence.

PROFESSIONAL SUMMARY:
{summary}

AVAILABLE EVIDENCE:

Accomplishments:
{accomplishments}

Experiences:
{experiences}

Metrics:
{metrics}

VERIFICATION RULES:
1. CONSERVATIVE APPROACH: Flag anything questionable
2. Quantifiable claims (percentages, dollar amounts) MUST have exact evidence
3. Years of experience must match date ranges in evidence
4. Skills mentioned must appear in evidence
5. Job titles must match what's in evidence
6. Industry/domain claims must be supported

For each unsupported or questionable claim, return:
- claim: the exact text from summary
- reason: why it's unsupported (no_evidence, weak_evidence, quantification_unsupported, date_mismatch, skill_level_mismatch)
- severity: low/medium/high
- explanation: brief explanation
- suggestion: how to fix it

Return JSON array format:
[{{"claim": "...", "reason": "...", "severity": "...", "explanation": "...", "suggestion": "..."}}]

If everything is supported, return: []"""

        message = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text.strip()

        # Parse JSON response
        import json
        try:
            issues = json.loads(response_text)
            flags = []
            for issue in issues:
                flags.append({
                    "resume_version_id": resume_version_id,
                    "section": "summary",
                    "claim_text": issue['claim'],
                    "flag_reason": issue['reason'],
                    "severity": issue['severity'],
                    "explanation": issue['explanation'],
                    "suggested_fix": issue['suggestion'],
                    "auto_flagged": True
                })
            return flags
        except:
            return []

    async def _verify_experience(
        self,
        experience: Dict,
        knowledge_base: List[Dict],
        resume_version_id: str,
        exp_idx: int
    ) -> List[Dict]:
        """Verify work experience bullets against evidence"""

        # Find relevant knowledge base entries
        company = experience.get('company', '')
        start_date = experience.get('start_date', '')
        end_date = experience.get('end_date', '')

        # Get relevant accomplishments and stories for this time period/company
        relevant_entries = [
            entry for entry in knowledge_base
            if (entry['knowledge_type'] in ['accomplishment', 'story', 'metric'])
            and (company.lower() in str(entry.get('content', '')).lower() or
                 self._date_overlaps(entry.get('date_range'), start_date, end_date))
        ]

        evidence = "\n".join([
            f"- {entry['title']}: {entry['content']}"
            for entry in relevant_entries
        ])

        bullets_text = "\n".join(experience['bullets'])

        prompt = f"""You are a truth verification expert for resume accuracy.

Verify these work experience bullets against available evidence.

POSITION: {experience['title']} at {company}
DATES: {start_date} - {end_date}

BULLETS TO VERIFY:
{bullets_text}

AVAILABLE EVIDENCE:
{evidence if evidence else "No specific evidence found for this position"}

VERIFICATION RULES:
1. Every quantified claim (numbers, percentages, dollars) MUST have specific evidence
2. Team sizes must be supported
3. Technologies/tools mentioned must appear in evidence
4. Achievements must have backing evidence
5. If no evidence exists for a position at all, flag it as HIGH severity
6. Round numbers without evidence = medium severity
7. Vague claims without numbers = low severity if no evidence

For each unsupported bullet or claim, return:
- bullet_index: which bullet (0-indexed)
- claim: the specific unsupported part
- reason: no_evidence, weak_evidence, quantification_unsupported, date_mismatch, skill_level_mismatch, conflicting_information
- severity: low/medium/high
- explanation: why it's flagged
- suggestion: how to fix or what evidence is needed

Return JSON array. If all bullets supported, return: []"""

        message = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text.strip()

        import json
        try:
            issues = json.loads(response_text)
            flags = []
            for issue in issues:
                bullet_idx = issue.get('bullet_index', 0)
                bullet_text = experience['bullets'][bullet_idx] if bullet_idx < len(experience['bullets']) else ""

                flags.append({
                    "resume_version_id": resume_version_id,
                    "section": f"experience_{exp_idx}",
                    "claim_text": issue['claim'],
                    "context": bullet_text,
                    "flag_reason": issue['reason'],
                    "severity": issue['severity'],
                    "explanation": issue['explanation'],
                    "suggested_fix": issue['suggestion'],
                    "auto_flagged": True
                })
            return flags
        except:
            return []

    async def _verify_skills(
        self,
        skills: Dict[str, List[str]],
        knowledge_base: List[Dict],
        resume_version_id: str
    ) -> List[Dict]:
        """Verify skills against knowledge base evidence"""

        # Get all skills from knowledge base
        kb_skills = [
            entry['title']
            for entry in knowledge_base
            if entry['knowledge_type'] == 'skill'
        ]

        # Also check if skills are mentioned in accomplishments/experiences
        all_kb_text = " ".join([
            str(entry.get('content', '')) + " " + str(entry.get('title', ''))
            for entry in knowledge_base
        ]).lower()

        flags = []
        all_resume_skills = []
        for category, skill_list in skills.items():
            all_resume_skills.extend(skill_list)

        # Check each skill
        for skill in all_resume_skills:
            skill_lower = skill.lower()

            # Check if skill is in knowledge base or mentioned in evidence
            in_kb_skills = any(skill_lower in kb_skill.lower() for kb_skill in kb_skills)
            mentioned_in_evidence = skill_lower in all_kb_text

            if not in_kb_skills and not mentioned_in_evidence:
                flags.append({
                    "resume_version_id": resume_version_id,
                    "section": "skills",
                    "claim_text": skill,
                    "flag_reason": "no_evidence",
                    "severity": "low",  # Skills without evidence = low severity (may be general skills)
                    "explanation": f"Skill '{skill}' not found in knowledge base or evidence",
                    "suggested_fix": "Add evidence of this skill through accomplishments or remove if not applicable",
                    "auto_flagged": True
                })

        return flags

    async def _verify_education(
        self,
        education: List[Dict],
        knowledge_base: List[Dict],
        resume_version_id: str
    ) -> List[Dict]:
        """Verify education claims"""

        kb_education = [
            entry for entry in knowledge_base
            if entry['knowledge_type'] == 'education'
        ]

        flags = []

        for edu in education:
            degree = edu.get('degree', '')
            institution = edu.get('institution', '')

            # Check if this education exists in knowledge base
            matching = [
                kb_edu for kb_edu in kb_education
                if (institution.lower() in str(kb_edu.get('content', '')).lower() or
                    institution.lower() in kb_edu.get('title', '').lower())
            ]

            if not matching:
                flags.append({
                    "resume_version_id": resume_version_id,
                    "section": "education",
                    "claim_text": f"{degree} from {institution}",
                    "flag_reason": "no_evidence",
                    "severity": "high",  # Education without evidence is serious
                    "explanation": "No evidence of this degree in knowledge base",
                    "suggested_fix": "Add education entry to knowledge base or verify accuracy",
                    "auto_flagged": True
                })

        return flags

    async def _verify_certifications(
        self,
        certifications: List[Dict],
        knowledge_base: List[Dict],
        resume_version_id: str
    ) -> List[Dict]:
        """Verify certification claims"""

        kb_certs = [
            entry for entry in knowledge_base
            if entry['knowledge_type'] == 'certification'
        ]

        flags = []

        for cert in certifications:
            cert_name = cert.get('name', '')

            # Check if certification exists in knowledge base
            matching = [
                kb_cert for kb_cert in kb_certs
                if cert_name.lower() in kb_cert.get('title', '').lower()
            ]

            if not matching:
                flags.append({
                    "resume_version_id": resume_version_id,
                    "section": "certifications",
                    "claim_text": cert_name,
                    "flag_reason": "no_evidence",
                    "severity": "high",  # Certifications are verifiable, so high severity
                    "explanation": "No evidence of this certification in knowledge base",
                    "suggested_fix": "Add certification to knowledge base or remove from resume",
                    "auto_flagged": True
                })

        return flags

    def _date_overlaps(self, date_range: str, start_date: str, end_date: str) -> bool:
        """Check if a date range overlaps with given dates"""
        if not date_range or not start_date:
            return False

        # Simple overlap check - can be improved with proper date parsing
        try:
            range_dates = date_range.strip('[]()').split(',')
            range_start = range_dates[0]
            range_end = range_dates[1] if len(range_dates) > 1 else "9999-12-31"

            # Basic string comparison (works for ISO dates)
            overlaps = (range_start <= end_date and range_end >= start_date)
            return overlaps
        except:
            return False

    async def _store_flags(self, flags: List[Dict]) -> None:
        """Store truth check flags in database"""
        if not flags:
            return

        try:
            self.supabase.table("truth_check_flags").insert(flags).execute()
        except Exception as e:
            print(f"Error storing flags: {e}")

    async def get_flags_for_resume(self, resume_version_id: str) -> List[Dict]:
        """Retrieve all flags for a resume version"""
        result = self.supabase.table("truth_check_flags")\
            .select("*")\
            .eq("resume_version_id", resume_version_id)\
            .order("severity", desc=True)\
            .order("created_at", desc=False)\
            .execute()

        return result.data

    async def resolve_flag(
        self,
        flag_id: str,
        resolution: str,
        resolved_by: str
    ) -> bool:
        """Mark a flag as resolved"""
        try:
            self.supabase.table("truth_check_flags")\
                .update({
                    "resolved": True,
                    "resolution_notes": resolution,
                    "resolved_at": datetime.utcnow().isoformat(),
                    "resolved_by": resolved_by
                })\
                .eq("id", flag_id)\
                .execute()
            return True
        except:
            return False

    async def get_verification_summary(self, user_id: str) -> Dict[str, Any]:
        """Get overall verification statistics for a user"""

        # Get all resume versions for user
        resumes_result = self.supabase.table("resume_versions")\
            .select("id")\
            .eq("user_id", user_id)\
            .execute()

        resume_ids = [r['id'] for r in resumes_result.data]

        if not resume_ids:
            return {
                "total_resumes": 0,
                "total_flags": 0,
                "unresolved_flags": 0,
                "severity_breakdown": {"low": 0, "medium": 0, "high": 0}
            }

        # Get all flags for these resumes
        flags_result = self.supabase.table("truth_check_flags")\
            .select("*")\
            .in_("resume_version_id", resume_ids)\
            .execute()

        flags = flags_result.data
        unresolved = [f for f in flags if not f.get('resolved', False)]

        severity_breakdown = {"low": 0, "medium": 0, "high": 0}
        for flag in unresolved:
            severity_breakdown[flag['severity']] += 1

        return {
            "total_resumes": len(resume_ids),
            "total_flags": len(flags),
            "unresolved_flags": len(unresolved),
            "severity_breakdown": severity_breakdown,
            "truth_score": self._calculate_truth_score(flags, resume_ids)
        }

    def _calculate_truth_score(self, flags: List[Dict], resume_ids: List[str]) -> float:
        """Calculate overall truth score (0-100)"""
        if not resume_ids:
            return 100.0

        # Score based on flag severity
        # high = -10 points, medium = -5 points, low = -2 points
        deductions = 0
        for flag in flags:
            if not flag.get('resolved', False):
                if flag['severity'] == 'high':
                    deductions += 10
                elif flag['severity'] == 'medium':
                    deductions += 5
                else:
                    deductions += 2

        # Normalize per resume
        avg_deduction = deductions / len(resume_ids)

        # Cap at 0-100
        score = max(0, min(100, 100 - avg_deduction))

        return round(score, 1)
