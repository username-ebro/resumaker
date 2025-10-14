"""
ATS Detection Service
Identifies which Applicant Tracking System (ATS) a job posting uses
Provides system-specific optimization recommendations
"""
from typing import Dict, Any, Optional, Tuple
import re
from urllib.parse import urlparse

class ATSDetectionService:
    """
    Detects ATS systems from job URLs and HTML content
    Provides tailored recommendations for each system
    """

    def __init__(self):
        # Known ATS systems with URL patterns and HTML signatures
        self.ats_systems = {
            "workday": {
                "url_patterns": [
                    r"myworkdayjobs\.com",
                    r"workday\.com/jobs",
                    r"wd1\.myworkdayjobs\.com",
                    r"wd5\.myworkdayjobs\.com"
                ],
                "html_signatures": [
                    "workday",
                    "wd-template",
                    "gwt-workday"
                ],
                "confidence_boost": 0.9,  # URL match is very reliable
                "recommendations": [
                    "Use 'Apply with LinkedIn' option if available for fastest processing",
                    "Create a separate Workday profile for this employer",
                    "Answer knockout questions very carefully - they auto-reject",
                    "System auto-fills data from your profile - review before submitting",
                    "Common issues: Date format must be MM/DD/YYYY"
                ],
                "optimal_format": "DOCX or LinkedIn",
                "parsing_quality": "excellent"
            },
            "greenhouse": {
                "url_patterns": [
                    r"greenhouse\.io",
                    r"boards\.greenhouse\.io",
                    r"grnh\.se"
                ],
                "html_signatures": [
                    "greenhouse",
                    "lever-frame",
                    "grnhse_app"
                ],
                "confidence_boost": 0.95,
                "recommendations": [
                    "Modern parsing - PDF files work well",
                    "Clean, simple format is best",
                    "System handles referrals well - mention if you have one",
                    "Cover letter highly visible to recruiters",
                    "Can save application and return later"
                ],
                "optimal_format": "PDF or DOCX",
                "parsing_quality": "excellent"
            },
            "lever": {
                "url_patterns": [
                    r"lever\.co",
                    r"jobs\.lever\.co"
                ],
                "html_signatures": [
                    "lever-job",
                    "lever-apply",
                    "lever-frame"
                ],
                "confidence_boost": 0.95,
                "recommendations": [
                    "Emphasizes relationships - mention referrals prominently",
                    "Modern system handles standard PDFs well",
                    "Include portfolio link if relevant - highly visible",
                    "Easy to apply with LinkedIn profile",
                    "Supports plain text and rich formatting equally well"
                ],
                "optimal_format": "PDF",
                "parsing_quality": "excellent"
            },
            "taleo": {
                "url_patterns": [
                    r"taleo\.net",
                    r"tbe\.taleo\.net"
                ],
                "html_signatures": [
                    "taleo",
                    "taleoForm",
                    "ftlOutput"
                ],
                "confidence_boost": 0.85,
                "recommendations": [
                    "CRITICAL: Use DOCX format - Taleo struggles with PDFs",
                    "Keep formatting EXTREMELY simple - no tables, columns, or text boxes",
                    "Avoid special characters or symbols (bullets should be simple)",
                    "Use standard fonts only (Arial, Times New Roman, Calibri)",
                    "One column layout is essential",
                    "System is older - expect application to take 20-30 minutes",
                    "Save frequently - system times out easily"
                ],
                "optimal_format": "DOCX (simple formatting)",
                "parsing_quality": "poor"
            },
            "icims": {
                "url_patterns": [
                    r"icims\.com",
                    r"careers\.icims\.com"
                ],
                "html_signatures": [
                    "icims",
                    "iCIMS",
                    "icimsprofile"
                ],
                "confidence_boost": 0.85,
                "recommendations": [
                    "Use traditional DOCX format",
                    "Keep layout simple - older parsing technology",
                    "Ensure consistent date formatting (MM/YYYY)",
                    "System auto-fills from previous applications",
                    "Check pre-populated data carefully",
                    "Application process can be lengthy"
                ],
                "optimal_format": "DOCX",
                "parsing_quality": "fair"
            },
            "smartrecruiters": {
                "url_patterns": [
                    r"smartrecruiters\.com",
                    r"jobs\.smartrecruiters\.com"
                ],
                "html_signatures": [
                    "smartrecruiters",
                    "sr-app",
                    "st-apply"
                ],
                "confidence_boost": 0.9,
                "recommendations": [
                    "Modern system with good PDF parsing",
                    "Mobile-friendly application process",
                    "Can apply with LinkedIn easily",
                    "Resume preview available before submission",
                    "Standard formatting works well"
                ],
                "optimal_format": "PDF or DOCX",
                "parsing_quality": "good"
            },
            "jobvite": {
                "url_patterns": [
                    r"jobvite\.com",
                    r"jobs\.jobvite\.com"
                ],
                "html_signatures": [
                    "jobvite",
                    "jv-apply",
                    "jvapplication"
                ],
                "confidence_boost": 0.9,
                "recommendations": [
                    "Good parsing for standard formats",
                    "Social media integration available",
                    "Can refer others for bonus (if applicable)",
                    "Application status tracking available",
                    "PDF and DOCX both work well"
                ],
                "optimal_format": "PDF or DOCX",
                "parsing_quality": "good"
            },
            "ashby": {
                "url_patterns": [
                    r"ashbyhq\.com",
                    r"jobs\.ashbyhq\.com"
                ],
                "html_signatures": [
                    "ashby",
                    "ashby-jobs"
                ],
                "confidence_boost": 0.95,
                "recommendations": [
                    "Modern, startup-focused ATS",
                    "Excellent PDF parsing",
                    "Clean, simple application process",
                    "Often used by tech companies",
                    "Fast application - minimal friction"
                ],
                "optimal_format": "PDF",
                "parsing_quality": "excellent"
            },
            "bamboohr": {
                "url_patterns": [
                    r"bamboohr\.com/jobs"
                ],
                "html_signatures": [
                    "bamboohr",
                    "bamboo-career"
                ],
                "confidence_boost": 0.9,
                "recommendations": [
                    "Small to mid-size company favorite",
                    "Simple application process",
                    "Standard formats work well",
                    "Often indicates company culture focus"
                ],
                "optimal_format": "PDF or DOCX",
                "parsing_quality": "good"
            },
            "linkedin": {
                "url_patterns": [
                    r"linkedin\.com/jobs"
                ],
                "html_signatures": [
                    "linkedin-job",
                    "jobs-apply-button"
                ],
                "confidence_boost": 1.0,
                "recommendations": [
                    "Apply with LinkedIn profile for instant application",
                    "Ensure your LinkedIn is up-to-date and complete",
                    "Can still upload custom resume",
                    "Many employers use 'Easy Apply' feature",
                    "Profile completeness affects visibility"
                ],
                "optimal_format": "LinkedIn profile (or PDF)",
                "parsing_quality": "excellent"
            }
        }

    def detect_ats(
        self,
        job_url: Optional[str] = None,
        html_content: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Detect ATS system from job URL and/or HTML content

        Args:
            job_url: URL of the job posting
            html_content: HTML content of the job posting page

        Returns:
            Dictionary with detection results:
            {
                "ats_system": str or None,
                "confidence": float (0.0-1.0),
                "detection_method": "url" | "html" | "both" | "none",
                "recommendations": List[str],
                "optimal_format": str,
                "parsing_quality": str
            }
        """

        if not job_url and not html_content:
            return self._no_detection_result()

        detected_system = None
        confidence = 0.0
        detection_method = "none"

        # Try URL detection first (most reliable)
        if job_url:
            url_result = self._detect_from_url(job_url)
            if url_result:
                detected_system = url_result["system"]
                confidence = url_result["confidence"]
                detection_method = "url"

        # Try HTML detection if URL didn't work or to boost confidence
        if html_content:
            html_result = self._detect_from_html(html_content)
            if html_result:
                if not detected_system:
                    detected_system = html_result["system"]
                    confidence = html_result["confidence"]
                    detection_method = "html"
                elif detected_system == html_result["system"]:
                    # Both methods agree - boost confidence
                    confidence = min(1.0, confidence + 0.1)
                    detection_method = "both"

        if detected_system:
            system_info = self.ats_systems[detected_system]
            return {
                "ats_system": detected_system,
                "confidence": round(confidence, 2),
                "detection_method": detection_method,
                "recommendations": system_info["recommendations"],
                "optimal_format": system_info["optimal_format"],
                "parsing_quality": system_info["parsing_quality"],
                "system_name": self._format_system_name(detected_system)
            }
        else:
            return self._no_detection_result()

    def _detect_from_url(self, job_url: str) -> Optional[Dict[str, Any]]:
        """Detect ATS system from URL patterns"""

        url_lower = job_url.lower()

        for system_name, system_info in self.ats_systems.items():
            for pattern in system_info["url_patterns"]:
                if re.search(pattern, url_lower):
                    return {
                        "system": system_name,
                        "confidence": system_info["confidence_boost"]
                    }

        return None

    def _detect_from_html(self, html_content: str) -> Optional[Dict[str, Any]]:
        """Detect ATS system from HTML signatures"""

        html_lower = html_content.lower()

        # Track matches and their scores
        matches = {}

        for system_name, system_info in self.ats_systems.items():
            match_count = 0
            for signature in system_info["html_signatures"]:
                if signature.lower() in html_lower:
                    match_count += 1

            if match_count > 0:
                # Confidence based on number of signature matches
                base_confidence = 0.5
                signature_boost = (match_count / len(system_info["html_signatures"])) * 0.3
                matches[system_name] = base_confidence + signature_boost

        if matches:
            # Return system with highest confidence
            best_match = max(matches.items(), key=lambda x: x[1])
            return {
                "system": best_match[0],
                "confidence": best_match[1]
            }

        return None

    def _no_detection_result(self) -> Dict[str, Any]:
        """Return result when ATS system cannot be detected"""
        return {
            "ats_system": None,
            "confidence": 0.0,
            "detection_method": "none",
            "recommendations": [
                "Use standard ATS-friendly format",
                "DOCX is universally safe choice",
                "Keep formatting simple and clean",
                "Use standard section headings",
                "Avoid tables, text boxes, and columns",
                "Test with online ATS checkers if possible"
            ],
            "optimal_format": "DOCX (simple formatting)",
            "parsing_quality": "unknown",
            "system_name": "Unknown ATS"
        }

    def _format_system_name(self, system_key: str) -> str:
        """Format system key to human-readable name"""
        name_map = {
            "workday": "Workday",
            "greenhouse": "Greenhouse",
            "lever": "Lever",
            "taleo": "Oracle Taleo",
            "icims": "iCIMS",
            "smartrecruiters": "SmartRecruiters",
            "jobvite": "Jobvite",
            "ashby": "Ashby",
            "bamboohr": "BambooHR",
            "linkedin": "LinkedIn"
        }
        return name_map.get(system_key, system_key.title())

    def get_format_recommendations(self, ats_system: Optional[str]) -> Dict[str, Any]:
        """
        Get detailed format recommendations for a specific ATS

        Args:
            ats_system: Name of the ATS system

        Returns:
            Detailed formatting guidelines
        """

        if not ats_system or ats_system not in self.ats_systems:
            return {
                "file_format": "DOCX",
                "fonts": ["Arial", "Calibri", "Times New Roman"],
                "font_size": "10-12pt",
                "margins": "0.5-1 inch",
                "sections": ["Contact", "Summary", "Experience", "Education", "Skills"],
                "avoid": ["Tables", "Text boxes", "Columns", "Headers/Footers", "Images"]
            }

        system_info = self.ats_systems[ats_system]

        # System-specific recommendations
        if ats_system == "taleo":
            return {
                "file_format": "DOCX only",
                "fonts": ["Arial", "Times New Roman"],
                "font_size": "11-12pt",
                "margins": "1 inch all sides",
                "sections": ["Contact", "Summary", "Experience", "Education", "Skills"],
                "avoid": [
                    "PDF format",
                    "Tables",
                    "Text boxes",
                    "Columns",
                    "Headers/Footers",
                    "Images",
                    "Special characters",
                    "Complex formatting"
                ],
                "critical": "Simplest possible formatting - Taleo has very poor parsing"
            }
        elif ats_system in ["greenhouse", "lever", "ashby"]:
            return {
                "file_format": "PDF or DOCX",
                "fonts": ["Any professional font"],
                "font_size": "10-12pt",
                "margins": "0.5-1 inch",
                "sections": ["Standard sections work well"],
                "avoid": ["Excessive graphics", "Unusual layouts"],
                "critical": "Modern system - most formats work well"
            }
        else:
            return {
                "file_format": system_info["optimal_format"],
                "fonts": ["Arial", "Calibri", "Helvetica"],
                "font_size": "10-12pt",
                "margins": "0.5-1 inch",
                "sections": ["Contact", "Summary", "Experience", "Education", "Skills"],
                "avoid": ["Complex tables", "Unusual fonts", "Heavy graphics"]
            }

    def compare_ats_systems(self, systems: list) -> Dict[str, Any]:
        """
        Compare multiple ATS systems

        Args:
            systems: List of ATS system names

        Returns:
            Comparison matrix
        """

        comparison = {
            "systems": [],
            "parsing_quality_ranking": [],
            "ease_of_use_ranking": []
        }

        for system in systems:
            if system in self.ats_systems:
                info = self.ats_systems[system]
                comparison["systems"].append({
                    "name": self._format_system_name(system),
                    "parsing_quality": info["parsing_quality"],
                    "optimal_format": info["optimal_format"],
                    "num_recommendations": len(info["recommendations"])
                })

        # Sort by parsing quality
        quality_order = {"excellent": 0, "good": 1, "fair": 2, "poor": 3}
        comparison["systems"].sort(
            key=lambda x: quality_order.get(x["parsing_quality"], 4)
        )

        return comparison


# Singleton instance
ats_detection_service = ATSDetectionService()
