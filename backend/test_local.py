"""
Local testing script for Resumaker backend
Tests all critical endpoints to verify functionality before deployment
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n🔍 Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_root():
    """Test root endpoint"""
    print("\n🔍 Testing / endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_signup():
    """Test user signup"""
    print("\n🔍 Testing /auth/signup endpoint...")
    test_user = {
        "email": f"test_{datetime.now().timestamp()}@example.com",
        "password": "TestPassword123!",
        "full_name": "Test User"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=test_user, timeout=5)
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 RESUMAKER BACKEND LOCAL TESTING")
    print("=" * 60)
    print(f"📍 Base URL: {BASE_URL}")
    print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = {
        "Root Endpoint": test_root(),
        "Health Check": test_health(),
        "User Signup": test_signup()
    }

    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")

    total = len(results)
    passed = sum(results.values())
    print(f"\n📈 Results: {passed}/{total} tests passed ({int(passed/total*100)}%)")

    if passed == total:
        print("\n🎉 All tests passed! Backend is working locally.")
    else:
        print("\n⚠️  Some tests failed. Check errors above.")

if __name__ == "__main__":
    main()
