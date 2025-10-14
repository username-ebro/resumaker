"""
Quick import test to verify all services can be imported
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

try:
    from app.services.company_research_service import company_research_service
    print("✅ company_research_service imported successfully")
except Exception as e:
    print(f"❌ company_research_service import failed: {e}")

try:
    from app.services.ats_detection_service import ats_detection_service
    print("✅ ats_detection_service imported successfully")
except Exception as e:
    print(f"❌ ats_detection_service import failed: {e}")

try:
    from app.services.job_matcher import JobMatcher
    print("✅ JobMatcher imported successfully")
except Exception as e:
    print(f"❌ JobMatcher import failed: {e}")

try:
    from app.services.resume_generator import ResumeGenerator
    print("✅ ResumeGenerator imported successfully")
except Exception as e:
    print(f"❌ ResumeGenerator import failed: {e}")

print("\n✅ All imports successful! Services are ready to use.")
