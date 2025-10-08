#!/usr/bin/env python3
"""Test Gemini Python SDK for OCR capability"""

import os
import sys

try:
    import google.generativeai as genai
    print("✅ google-generativeai package imported successfully")
except ImportError:
    print("❌ google-generativeai not installed")
    print("Installing now...")
    os.system("pip3 install google-generativeai")
    import google.generativeai as genai

# Configure API key
GEMINI_API_KEY = "AIzaSyDc9DnX2ed4eyL0LcBnDT-Q9oaCCp7nUzg"
genai.configure(api_key=GEMINI_API_KEY)

# Test basic model initialization
try:
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    print("✅ Gemini model initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize model: {e}")
    sys.exit(1)

# Test text generation (no file needed)
try:
    response = model.generate_content("Say 'OCR test successful' if you can read this.")
    print(f"✅ Model response: {response.text}")
except Exception as e:
    print(f"❌ Failed to generate content: {e}")
    sys.exit(1)

print("\n🎉 Gemini Python SDK is working!")
print("Note: Full OCR test with PDF will be done in Phase 2")
