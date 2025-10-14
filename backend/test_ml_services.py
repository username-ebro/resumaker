"""
Test ML/AI Services
Run these tests to verify all intelligent services work correctly
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.company_research_service import company_research_service
from app.services.ats_detection_service import ats_detection_service
from app.services.job_matcher import JobMatcher
from app.services.resume_generator import ResumeGenerator

# Sample data for testing
SAMPLE_JOB_DESCRIPTION = """
Senior Software Engineer

We're looking for a Senior Software Engineer to join our team.

Requirements:
- 5+ years of professional software development experience
- Strong proficiency in Python and JavaScript
- Experience with React and Node.js
- Knowledge of AWS or similar cloud platforms
- Bachelor's degree in Computer Science or related field

Preferred:
- Experience with Docker and Kubernetes
- Familiarity with CI/CD pipelines
- Previous startup experience
- Strong communication skills

About Us:
We're a fast-growing startup revolutionizing the e-commerce space.
"""

SAMPLE_COMPANY_NAME = "Acme Corporation"

SAMPLE_JOB_URLS = [
    "https://myworkdayjobs.com/acme/job/123456",
    "https://boards.greenhouse.io/acme/jobs/123456",
    "https://jobs.lever.co/acme/123456",
    "https://careers.taleo.net/acme/job/123456",
]

SAMPLE_USER_PROMPT = "applying for a concession stand position at a baseball stadium"

SAMPLE_KNOWLEDGE_BASE = [
    {
        "knowledge_type": "skill",
        "title": "Python Programming",
        "content": {"skill_name": "Python", "years_experience": 5}
    },
    {
        "knowledge_type": "skill",
        "title": "Customer Service",
        "content": {"skill_name": "Customer Service", "years_experience": 3}
    },
    {
        "knowledge_type": "experience",
        "title": "Software Engineer at Tech Co",
        "content": {"job_title": "Software Engineer", "company": "Tech Co"}
    },
    {
        "knowledge_type": "experience",
        "title": "Cashier at Local Store",
        "content": {"job_title": "Cashier", "company": "Local Store"}
    },
    {
        "knowledge_type": "skill",
        "title": "React Development",
        "content": {"skill_name": "React", "years_experience": 4}
    },
    {
        "knowledge_type": "skill",
        "title": "Cash Handling",
        "content": {"skill_name": "Cash Handling", "years_experience": 2}
    }
]


async def test_company_research():
    """Test company research service"""
    print("\n" + "="*60)
    print("TEST 1: Company Research Service")
    print("="*60)

    try:
        result = await company_research_service.research_company(
            company_name=SAMPLE_COMPANY_NAME
        )

        print(f"\nCompany: {result['company_name']}")
        print(f"Website: {result['website']}")
        print(f"LinkedIn: {result['linkedin']}")
        print(f"Industry: {result['industry']}")
        print(f"Values: {', '.join(result['values']) if result['values'] else 'None found'}")
        print(f"Culture: {', '.join(result['culture_keywords']) if result['culture_keywords'] else 'None found'}")
        print(f"Research Success: {result['research_success']}")

        # Test tailoring suggestions
        suggestions = company_research_service.get_tailoring_suggestions(result)
        print(f"\nTailoring Suggestions ({len(suggestions)}):")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")

        print("\n✅ Company Research Service: PASSED")
        return True

    except Exception as e:
        print(f"\n❌ Company Research Service: FAILED")
        print(f"Error: {str(e)}")
        return False


def test_ats_detection():
    """Test ATS detection service"""
    print("\n" + "="*60)
    print("TEST 2: ATS Detection Service")
    print("="*60)

    all_passed = True

    for url in SAMPLE_JOB_URLS:
        try:
            result = ats_detection_service.detect_ats(job_url=url)

            print(f"\nURL: {url}")
            print(f"Detected System: {result['system_name']}")
            print(f"Confidence: {result['confidence']}")
            print(f"Optimal Format: {result['optimal_format']}")
            print(f"Parsing Quality: {result['parsing_quality']}")
            print(f"Recommendations: {len(result['recommendations'])} tips")

            if result['ats_system']:
                print("  Sample recommendations:")
                for rec in result['recommendations'][:2]:
                    print(f"    - {rec}")

        except Exception as e:
            print(f"\n❌ Failed for URL: {url}")
            print(f"Error: {str(e)}")
            all_passed = False

    if all_passed:
        print("\n✅ ATS Detection Service: PASSED")
    else:
        print("\n❌ ATS Detection Service: FAILED")

    return all_passed


async def test_job_matcher():
    """Test enhanced job matcher service"""
    print("\n" + "="*60)
    print("TEST 3: Job Matcher Service (Enhanced)")
    print("="*60)

    try:
        job_matcher = JobMatcher()

        # Test 1: Enhanced keyword extraction
        print("\n--- Test 3A: Enhanced Keyword Extraction ---")
        keywords = await job_matcher.extract_keywords_with_ai(SAMPLE_JOB_DESCRIPTION)

        print(f"\nCritical Keywords: {keywords.get('critical', [])}")
        print(f"Important Keywords: {keywords.get('important', [])}")
        print(f"Nice-to-Have: {keywords.get('nice_to_have', [])}")
        print(f"Technical Skills: {keywords.get('technical', [])}")
        print(f"Soft Skills: {keywords.get('soft_skills', [])}")

        # Test 2: Requirement categorization
        print("\n--- Test 3B: Requirement Categorization ---")
        requirements = await job_matcher.categorize_requirements(SAMPLE_JOB_DESCRIPTION)

        print(f"\nMust-Have Skills: {requirements['must_have'].get('skills', [])}")
        print(f"Experience Years: {requirements['must_have'].get('experience_years', 'Not specified')}")
        print(f"Education: {requirements['must_have'].get('education', 'Not specified')}")
        print(f"\nNice-to-Have Skills: {requirements['nice_to_have'].get('skills', [])}")
        print(f"Deal Breakers: {requirements.get('deal_breakers', [])}")

        print("\n✅ Job Matcher Service: PASSED")
        return True

    except Exception as e:
        print(f"\n❌ Job Matcher Service: FAILED")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_resume_generator_generic_mode():
    """Test generic resume mode with fact selection"""
    print("\n" + "="*60)
    print("TEST 4: Resume Generator - Generic Mode")
    print("="*60)

    try:
        resume_gen = ResumeGenerator()

        print(f"\nUser Prompt: '{SAMPLE_USER_PROMPT}'")
        print(f"Total Facts Available: {len(SAMPLE_KNOWLEDGE_BASE)}")

        # Test fact selection
        print("\n--- Test 4A: Relevant Fact Selection ---")
        relevant_facts = await resume_gen.select_relevant_facts(
            user_prompt=SAMPLE_USER_PROMPT,
            all_entities=SAMPLE_KNOWLEDGE_BASE
        )

        print(f"Selected {len(relevant_facts)} relevant facts:")
        for fact in relevant_facts:
            print(f"  - [{fact['knowledge_type']}] {fact['title']}")

        # Test keyword extraction from prompt
        print("\n--- Test 4B: Keyword Extraction from Prompt ---")
        keywords = await resume_gen._extract_keywords_from_prompt(SAMPLE_USER_PROMPT)
        print(f"Keywords: {', '.join(keywords)}")

        print("\n✅ Resume Generator Generic Mode: PASSED")
        return True

    except Exception as e:
        print(f"\n❌ Resume Generator Generic Mode: FAILED")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def run_all_tests():
    """Run all ML/AI service tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "ML/AI SERVICES TEST SUITE" + " "*18 + "║")
    print("╚" + "="*58 + "╝")

    results = []

    # Test 1: Company Research
    results.append(await test_company_research())

    # Test 2: ATS Detection
    results.append(test_ats_detection())

    # Test 3: Job Matcher Enhanced
    results.append(await test_job_matcher())

    # Test 4: Resume Generator Generic Mode
    results.append(await test_resume_generator_generic_mode())

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    test_names = [
        "Company Research Service",
        "ATS Detection Service",
        "Job Matcher Enhanced",
        "Resume Generator Generic Mode"
    ]

    for name, passed in zip(test_names, results):
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name}: {status}")

    passed_count = sum(results)
    total_count = len(results)

    print(f"\nTotal: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
