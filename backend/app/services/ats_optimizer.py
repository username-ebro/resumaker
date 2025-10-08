"""
ATS Optimizer Service
Applies ATS formatting rules and optimization strategies
"""
from typing import Dict, Any, List
import re

class ATSOptimizer:
    """Applies ATS best practices from the 2025 guide"""

    def __init__(self):
        # ATS-safe fonts
        self.safe_fonts = [
            "Arial", "Calibri", "Helvetica",
            "Times New Roman", "Rubik", "Lato"
        ]

        # Standard section headings ATS recognizes
        self.standard_headings = {
            "summary": ["Professional Summary", "Summary", "Profile"],
            "experience": ["Professional Experience", "Work Experience", "Experience"],
            "skills": ["Skills", "Core Competencies", "Technical Skills"],
            "education": ["Education"],
            "certifications": ["Certifications", "Certifications & Credentials"]
        }

        # Strong action verbs by category
        self.action_verbs = {
            "leadership": ["Directed", "Led", "Managed", "Supervised", "Orchestrated", "Spearheaded", "Championed", "Drove"],
            "achievement": ["Achieved", "Improved", "Increased", "Enhanced", "Optimized", "Accelerated", "Strengthened", "Elevated"],
            "creation": ["Developed", "Created", "Designed", "Built", "Launched", "Pioneered", "Established", "Engineered"],
            "problem_solving": ["Resolved", "Streamlined", "Simplified", "Consolidated", "Transformed", "Restructured", "Overhauled"],
            "analysis": ["Analyzed", "Evaluated", "Assessed", "Forecasted", "Identified", "Researched", "Strategized"]
        }

    def optimize_resume(self, resume_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply ATS optimization rules to resume structure

        Returns optimized resume with ATS compliance score
        """
        optimized = resume_structure.copy()
        optimization_report = {
            "ats_score": 0,
            "improvements_made": [],
            "warnings": [],
            "recommendations": []
        }

        # 1. Optimize contact info
        optimized['contact_info'], contact_score = self._optimize_contact_info(
            resume_structure.get('contact_info', {})
        )
        optimization_report['ats_score'] += contact_score

        # 2. Optimize summary
        optimized['summary'], summary_score, summary_improvements = self._optimize_summary(
            resume_structure.get('summary', '')
        )
        optimization_report['ats_score'] += summary_score
        optimization_report['improvements_made'].extend(summary_improvements)

        # 3. Optimize experience bullets
        optimized['experience'], exp_score, exp_improvements = self._optimize_experience(
            resume_structure.get('experience', [])
        )
        optimization_report['ats_score'] += exp_score
        optimization_report['improvements_made'].extend(exp_improvements)

        # 4. Check resume length
        length_warnings = self._check_resume_length(resume_structure)
        optimization_report['warnings'].extend(length_warnings)

        # 5. Generate recommendations
        recommendations = self._generate_recommendations(resume_structure)
        optimization_report['recommendations'].extend(recommendations)

        # Normalize score to 0-100
        optimization_report['ats_score'] = min(100, optimization_report['ats_score'])

        optimized['optimization_report'] = optimization_report

        return optimized

    def _optimize_contact_info(self, contact_info: Dict) -> tuple[Dict, int]:
        """Optimize contact information section"""
        score = 0
        optimized = contact_info.copy()

        # Check required fields
        if contact_info.get('name'):
            score += 10
        if contact_info.get('email'):
            score += 10
        if contact_info.get('phone'):
            score += 5

        # Optimize LinkedIn URL (remove https://)
        if contact_info.get('linkedin'):
            linkedin = contact_info['linkedin']
            # Clean up LinkedIn URL
            linkedin = linkedin.replace('https://', '').replace('http://', '')
            linkedin = linkedin.replace('www.', '')
            optimized['linkedin'] = linkedin
            score += 5

        # Location - prefer City, State format
        if contact_info.get('location'):
            score += 5

        return optimized, score

    def _optimize_summary(self, summary: str) -> tuple[str, int, List[str]]:
        """Optimize professional summary"""
        score = 0
        improvements = []
        optimized = summary

        # Check length (3-4 sentences ideal)
        sentences = summary.split('.')
        sentence_count = len([s for s in sentences if s.strip()])

        if 3 <= sentence_count <= 4:
            score += 15
        elif sentence_count < 3:
            improvements.append("Summary should be 3-4 sentences for optimal impact")
            score += 10
        else:
            improvements.append("Summary is too long - aim for 3-4 concise sentences")
            score += 10

        # Check for quantifiable achievements
        if re.search(r'\d+%|\$\d+|[\d,]+', summary):
            score += 10
            improvements.append("Good: Summary includes quantifiable achievements")
        else:
            improvements.append("Consider adding a quantifiable achievement to summary")

        # Check for action-oriented language
        has_action_verb = False
        for category_verbs in self.action_verbs.values():
            if any(verb.lower() in summary.lower() for verb in category_verbs):
                has_action_verb = True
                break

        if has_action_verb:
            score += 5
        else:
            improvements.append("Use stronger action verbs in summary")

        return optimized, score, improvements

    def _optimize_experience(self, experience: List[Dict]) -> tuple[List[Dict], int, List[str]]:
        """Optimize work experience section"""
        score = 0
        improvements = []
        optimized = []

        for exp in experience:
            opt_exp = exp.copy()
            exp_improvements = []

            # Check date format
            if self._has_consistent_date_format(exp.get('start_date', ''), exp.get('end_date', '')):
                score += 2

            # Optimize bullets
            opt_bullets = []
            for bullet in exp.get('bullets', []):
                opt_bullet, bullet_score, bullet_improvements = self._optimize_bullet(bullet)
                opt_bullets.append(opt_bullet)
                score += bullet_score
                exp_improvements.extend(bullet_improvements)

            opt_exp['bullets'] = opt_bullets

            # Check bullet count (4-7 is ideal)
            bullet_count = len(opt_bullets)
            if 4 <= bullet_count <= 7:
                score += 3
            elif bullet_count < 4:
                exp_improvements.append(f"Add more bullets to {exp['title']} (4-7 recommended)")
            else:
                exp_improvements.append(f"Consider condensing bullets for {exp['title']} (4-7 recommended)")

            improvements.extend(exp_improvements)
            optimized.append(opt_exp)

        return optimized, score, improvements

    def _optimize_bullet(self, bullet: str) -> tuple[str, int, List[str]]:
        """Optimize individual bullet point"""
        score = 0
        improvements = []
        optimized = bullet.strip()

        # Ensure bullet starts with action verb
        starts_with_action_verb = False
        first_word = optimized.split()[0] if optimized else ""

        for category_verbs in self.action_verbs.values():
            if first_word in category_verbs:
                starts_with_action_verb = True
                score += 2
                break

        if not starts_with_action_verb:
            improvements.append(f"Bullet should start with strong action verb: '{optimized[:50]}...'")

        # Check for quantifiable results
        has_numbers = bool(re.search(r'\d+%|\$[\d,]+|[\d,]+\+?', optimized))
        if has_numbers:
            score += 3
            improvements.append("Good: Bullet includes quantifiable results")
        else:
            improvements.append(f"Add quantifiable result to: '{optimized[:50]}...'")

        # Check length (1-2 lines ideal, roughly 80-150 characters)
        if 80 <= len(optimized) <= 150:
            score += 2
        elif len(optimized) > 150:
            improvements.append(f"Bullet too long (>150 chars): '{optimized[:50]}...'")
        else:
            improvements.append(f"Bullet too short (<80 chars): '{optimized[:50]}...'")

        # Avoid weak phrases
        weak_phrases = ["responsible for", "tasked with", "helped to", "was involved in", "duties included"]
        for phrase in weak_phrases:
            if phrase in optimized.lower():
                improvements.append(f"Replace weak phrase '{phrase}' with action verb")
                score -= 1

        return optimized, max(0, score), improvements

    def _has_consistent_date_format(self, start: str, end: str) -> bool:
        """Check if dates follow consistent format"""
        if not start:
            return False

        # Check for "Month Year" format (ideal for ATS)
        pattern = r'^[A-Z][a-z]+ \d{4}$'  # e.g., "January 2021"

        start_match = bool(re.match(pattern, start))
        end_match = end == "Present" or bool(re.match(pattern, end))

        return start_match and end_match

    def _check_resume_length(self, resume: Dict) -> List[str]:
        """Check resume length and provide warnings"""
        warnings = []

        experience_count = len(resume.get('experience', []))
        total_bullets = sum(len(exp.get('bullets', [])) for exp in resume.get('experience', []))

        # Estimate page count
        # Rough estimate: ~15 bullets per page + sections
        estimated_pages = (total_bullets + 10) / 15

        if estimated_pages < 1:
            warnings.append("Resume may be too short - aim for 1-2 pages")
        elif estimated_pages > 2.5:
            warnings.append("Resume may be too long - try to keep to 2 pages max")

        return warnings

    def _generate_recommendations(self, resume: Dict) -> List[str]:
        """Generate ATS optimization recommendations"""
        recommendations = []

        # Check for skills section
        skills = resume.get('skills', {})
        if not skills:
            recommendations.append("HIGH PRIORITY: Add a Skills section with relevant keywords")
        else:
            total_skills = sum(len(skill_list) for skill_list in skills.values())
            if total_skills < 8:
                recommendations.append("Add more skills (aim for 10-15 total)")

        # Check for quantification
        exp_bullets = []
        for exp in resume.get('experience', []):
            exp_bullets.extend(exp.get('bullets', []))

        bullets_with_numbers = sum(1 for b in exp_bullets if re.search(r'\d', b))
        quantification_rate = bullets_with_numbers / len(exp_bullets) if exp_bullets else 0

        if quantification_rate < 0.5:
            recommendations.append("Add more quantifiable results (aim for 60-80% of bullets)")

        # Check for education
        if not resume.get('education'):
            recommendations.append("Add education section (if applicable)")

        # Check for certifications
        if not resume.get('certifications'):
            recommendations.append("Consider adding relevant certifications to stand out")

        return recommendations

    def check_ats_compatibility(self, html_resume: str) -> Dict[str, Any]:
        """
        Check HTML resume for ATS compatibility issues

        Returns report with warnings and recommendations
        """
        report = {
            "compatible": True,
            "warnings": [],
            "critical_issues": []
        }

        # Check for ATS-breaking elements
        if '<table' in html_resume.lower():
            report['critical_issues'].append("Contains tables - may cause parsing errors")
            report['compatible'] = False

        if '<img' in html_resume.lower():
            report['critical_issues'].append("Contains images - content will be lost in ATS")
            report['compatible'] = False

        if 'text-box' in html_resume.lower() or 'textbox' in html_resume.lower():
            report['critical_issues'].append("Contains text boxes - will scramble content")
            report['compatible'] = False

        # Check for multiple columns
        if 'column' in html_resume.lower() and 'multi' in html_resume.lower():
            report['warnings'].append("Multi-column layout may cause parsing issues")

        # Check font
        for safe_font in self.safe_fonts:
            if safe_font.lower() in html_resume.lower():
                break
        else:
            report['warnings'].append(f"Font may not be ATS-safe. Use: {', '.join(self.safe_fonts[:3])}")

        # Check font size
        if 'font-size: 9pt' in html_resume or 'font-size:9pt' in html_resume:
            report['warnings'].append("Font size too small (use 10-12pt)")

        return report

    def get_keyword_density(self, text: str, keywords: List[str]) -> Dict[str, Any]:
        """
        Calculate keyword density for ATS optimization

        Args:
            text: Resume text
            keywords: Target keywords from job description

        Returns:
            Dictionary with keyword analysis
        """
        text_lower = text.lower()
        word_count = len(text.split())

        keyword_matches = {}
        total_matches = 0

        for keyword in keywords:
            keyword_lower = keyword.lower()
            count = text_lower.count(keyword_lower)
            if count > 0:
                keyword_matches[keyword] = count
                total_matches += count

        match_rate = (len(keyword_matches) / len(keywords) * 100) if keywords else 0

        return {
            "total_keywords": len(keywords),
            "matched_keywords": len(keyword_matches),
            "match_rate": round(match_rate, 1),
            "keyword_details": keyword_matches,
            "total_occurrences": total_matches,
            "density": round((total_matches / word_count * 100), 2) if word_count > 0 else 0,
            "recommendation": self._get_match_rate_recommendation(match_rate)
        }

    def _get_match_rate_recommendation(self, match_rate: float) -> str:
        """Get recommendation based on keyword match rate"""
        if match_rate >= 80:
            return "Excellent keyword optimization! (80%+)"
        elif match_rate >= 75:
            return "Good keyword match (75-79%). You're likely to pass ATS filters."
        elif match_rate >= 65:
            return "Acceptable keyword match (65-74%). Consider adding a few more target keywords."
        elif match_rate >= 50:
            return "Low keyword match (50-64%). Add more relevant keywords from job description."
        else:
            return "Critical: Keyword match below 50%. Significant optimization needed."
