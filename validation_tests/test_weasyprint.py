#!/usr/bin/env python3
"""Test WeasyPrint PDF generation"""

import os
import sys

# Check system dependencies first
print("Checking system dependencies...")
os.system("brew list cairo pango gdk-pixbuf libffi 2>/dev/null || echo '⚠️  Missing system deps - will try to install'")

try:
    from weasyprint import HTML, CSS
    print("✅ weasyprint package imported successfully")
except ImportError:
    print("❌ weasyprint not installed")
    print("Installing now...")
    os.system("pip3 install weasyprint")
    try:
        from weasyprint import HTML, CSS
    except ImportError as e:
        print(f"❌ Still failed after install: {e}")
        print("You may need to install system dependencies:")
        print("  brew install cairo pango gdk-pixbuf libffi")
        sys.exit(1)

# Test PDF generation
try:
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #333; }
        </style>
    </head>
    <body>
        <h1>WeasyPrint Test</h1>
        <p>If you can read this PDF, WeasyPrint is working!</p>
    </body>
    </html>
    """

    output_path = "/Users/evanstoudt/Documents/File Cabinet/Coding/resumaker/validation_tests/test_output.pdf"
    HTML(string=html_content).write_pdf(output_path)
    print(f"✅ PDF generated successfully at: {output_path}")
except Exception as e:
    print(f"❌ Failed to generate PDF: {e}")
    sys.exit(1)

print("\n🎉 WeasyPrint is working!")
