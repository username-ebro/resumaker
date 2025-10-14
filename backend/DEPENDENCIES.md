# Resumaker Backend - Dependencies

## Installation Required

### Critical Dependency (MUST INSTALL)

```bash
pip install python-docx
```

**Why**: Required for DOCX file reading and writing
**Used by**:
- `app/services/ocr_service.py` - Extract text from uploaded .docx resumes
- `app/services/docx_exporter.py` - Generate downloadable Word resumes

**Without this**: DOCX upload and export will fail with ImportError

---

## Optional Dependencies

### For Legacy .doc File Support

```bash
# macOS
brew install antiword

# Ubuntu/Debian
sudo apt-get install antiword

# Red Hat/CentOS
sudo yum install antiword
```

**Why**: Converts old Microsoft Word .doc files to text
**Used by**: `app/services/ocr_service.py._extract_from_doc()`
**Without this**: .doc files will return error message, but .docx will still work

---

## Already Installed Dependencies

These are already in `requirements.txt` and installed:

### Core Framework
- `fastapi==0.115.5` - Web framework
- `uvicorn==0.34.0` - ASGI server
- `python-multipart==0.0.20` - File upload support

### Database
- `supabase==2.21.1` - Database client
- `psycopg2-binary==2.9.10` - PostgreSQL adapter

### AI/ML APIs
- `anthropic==0.40.0` - Claude API for resume generation
- `google-generativeai==0.8.3` - Gemini API for OCR

### Document Generation
- `weasyprint==66.0` - PDF generation
- `python-docx==1.1.2` - **NEEDS INSTALL** (in requirements but may not be installed)
- `pillow==11.3.0` - Image processing

### Utilities
- `python-dotenv==1.0.1` - Environment variables
- `pydantic==2.10.5` - Data validation
- `python-jose==3.3.0` - JWT tokens

---

## Verify Installation

Run this to check all dependencies:

```bash
cd /Users/evanstoudt/Documents/File\ Cabinet/Coding/resumaker/backend

# Check if python-docx is installed
python3 -c "from docx import Document; print('✅ python-docx installed')" || echo "❌ python-docx NOT installed"

# Check if antiword is available (optional)
which antiword && echo "✅ antiword installed" || echo "⚠️ antiword not installed (optional)"

# Check Claude API key
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); key=os.getenv('CLAUDE_API_KEY'); print('✅ Claude API key found' if key else '❌ Claude API key missing')"

# Check Gemini API key
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); key=os.getenv('GEMINI_API_KEY'); print('✅ Gemini API key found' if key else '❌ Gemini API key missing')"
```

---

## Quick Setup

Run this to install all missing dependencies:

```bash
cd /Users/evanstoudt/Documents/File\ Cabinet/Coding/resumaker/backend

# Install Python dependencies
pip install -r requirements.txt

# Install python-docx explicitly (if not already installed)
pip install python-docx

# Optional: Install antiword for .doc support
brew install antiword  # macOS
# or
sudo apt-get install antiword  # Linux
```

---

## Environment Variables

Make sure `.env` file has these set:

```bash
# Required
CLAUDE_API_KEY=sk-ant-api03-...
GEMINI_API_KEY=AIzaSy...
SUPABASE_URL=https://....supabase.co
SUPABASE_SECRET_KEY=eyJhbGc...

# Optional
DYLD_LIBRARY_PATH=/opt/homebrew/lib  # macOS for WeasyPrint
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'docx'"

**Solution**:
```bash
pip install python-docx
```

### Issue: "Could not extract text from .doc file"

**Solution**: Install antiword
```bash
brew install antiword  # macOS
```

Or use .docx format instead (recommended)

### Issue: WeasyPrint fails with "cannot load library"

**Solution** (macOS):
```bash
brew install pango gdk-pixbuf libffi
export DYLD_LIBRARY_PATH=/opt/homebrew/lib
```

Add to `.env`:
```
DYLD_LIBRARY_PATH=/opt/homebrew/lib
```

### Issue: Claude API calls fail

**Solution**: Check API key in `.env`:
```bash
cat .env | grep CLAUDE_API_KEY
```

Make sure key is valid and has credits.

---

## Production Considerations

### API Rate Limits

**Claude API**:
- Tier 1: 50 requests/minute
- Tier 2: 1000 requests/minute
- Each resume generation: 5-8 requests

**Recommendation**: Implement job queue (Celery + Redis) for async processing

### Caching

Consider caching:
- Job analysis results (same job URL)
- ATS system detection
- Knowledge base queries

### Database Connection Pooling

For production, configure connection pooling:
```python
# In app/database.py
from sqlalchemy import create_engine
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20
)
```

---

## Memory Usage

Typical memory usage:
- Base FastAPI app: ~100MB
- Per resume generation: +50-100MB (Claude API responses)
- PDF generation: +30-50MB (WeasyPrint)
- DOCX generation: +20-30MB (python-docx)

**Recommended**: 1GB RAM minimum, 2GB for production

---

## File Storage

Current implementation uses temporary files:
- Upload directory: `./uploads/` (auto-created)
- Temporary files deleted after processing

**Production TODO**:
- Use cloud storage (S3, Supabase Storage)
- Implement file size limits (currently 10MB max)
- Add virus scanning for uploads
