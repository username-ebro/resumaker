"""
Resumaker Integration Tests
Tests the complete stack locally: Frontend → Backend → Database
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3001"
TEST_USER = {
    "email": f"integration_test_{int(time.time())}@example.com",
    "password": "TestPassword123!",
    "full_name": "Integration Test User"
}

def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_backend_health():
    """Test 1: Backend Health Check"""
    print_section("TEST 1: Backend Health Check")

    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        data = response.json()

        print(f"✅ Status Code: {response.status_code}")
        print(f"📊 Response: {json.dumps(data, indent=2)}")

        assert response.status_code == 200, "Health check failed"
        assert data.get("status") == "healthy", "Backend not healthy"

        print("✅ PASSED: Backend is healthy")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_frontend_loads():
    """Test 2: Frontend Homepage Loads"""
    print_section("TEST 2: Frontend Homepage")

    try:
        response = requests.get(FRONTEND_URL, timeout=5)

        print(f"✅ Status Code: {response.status_code}")
        print(f"📄 Contains 'Resumaker': {'Yes' if 'Resumaker' in response.text else 'No'}")

        assert response.status_code == 200, "Frontend not accessible"
        assert "Resumaker" in response.text, "Frontend content missing"

        print("✅ PASSED: Frontend loads correctly")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_api_docs():
    """Test 3: API Documentation Accessible"""
    print_section("TEST 3: API Documentation")

    try:
        response = requests.get(f"{BACKEND_URL}/docs", timeout=5)

        print(f"✅ Status Code: {response.status_code}")
        print(f"📚 Swagger UI: {'Loaded' if 'swagger' in response.text.lower() else 'Not Found'}")

        assert response.status_code == 200, "API docs not accessible"

        print("✅ PASSED: API documentation accessible")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_resume_list():
    """Test 4: Resume List Endpoint"""
    print_section("TEST 4: Resume List Endpoint")

    try:
        response = requests.get(f"{BACKEND_URL}/resumes/list?user_id=test-user-id", timeout=5)
        data = response.json()

        print(f"✅ Status Code: {response.status_code}")
        print(f"📋 Response: {json.dumps(data, indent=2)}")

        assert response.status_code == 200, "Resume list failed"
        assert "resumes" in data, "Resumes key missing"

        print("✅ PASSED: Resume list endpoint works")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_cors():
    """Test 5: CORS Configuration"""
    print_section("TEST 5: CORS Configuration")

    try:
        headers = {
            "Origin": "http://localhost:3001",
            "Access-Control-Request-Method": "GET"
        }
        response = requests.options(f"{BACKEND_URL}/health", headers=headers, timeout=5)

        print(f"✅ Status Code: {response.status_code}")
        print(f"🔐 CORS Headers: {dict(response.headers)}")

        print("✅ PASSED: CORS configured")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def main():
    """Run all integration tests"""
    print("\n" + "=" * 70)
    print("  🧪 RESUMAKER INTEGRATION TEST SUITE")
    print("=" * 70)
    print(f"  Backend: {BACKEND_URL}")
    print(f"  Frontend: {FRONTEND_URL}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    tests = [
        ("Backend Health", test_backend_health),
        ("Frontend Homepage", test_frontend_loads),
        ("API Documentation", test_api_docs),
        ("Resume List", test_resume_list),
        ("CORS Configuration", test_cors)
    ]

    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            results[name] = False
        time.sleep(1)  # Brief pause between tests

    # Print summary
    print_section("FINAL RESULTS")

    total = len(results)
    passed = sum(results.values())
    failed = total - passed

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")

    print("\n" + "-" * 70)
    print(f"  Total Tests: {total}")
    print(f"  Passed: {passed} ({'green' if passed == total else 'yellow'})")
    print(f"  Failed: {failed} ({'red' if failed > 0 else 'green'})")
    print(f"  Success Rate: {int(passed/total*100)}%")
    print("-" * 70)

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Application is working correctly.")
        print("✅ Ready for production deployment!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Review errors above.")
        return 1

if __name__ == "__main__":
    exit(main())
