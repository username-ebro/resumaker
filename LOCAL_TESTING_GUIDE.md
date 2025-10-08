# 🏠 Resumaker Local Testing Guide

Complete guide for running and testing Resumaker locally before deployment.

---

## 🚀 Quick Start

###  1. Start Backend
```bash
cd backend
source ../venv/bin/activate
export DYLD_LIBRARY_PATH=/opt/homebrew/lib
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Start Frontend
```bash
cd frontend
npm run dev
```

### 3. Access Application
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 🧪 Running Tests

### Backend Health Check
```bash
curl http://localhost:8000/health | python3 -m json.tool
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "services": {
    "claude": "available",
    "gemini": "available",
    "supabase": "available"
  }
}
```

### Comprehensive Backend Tests
```bash
cd backend
source ../venv/bin/activate
python test_local.py
```

---

## 🔧 Environment Setup

### Backend Environment Variables
Located in `backend/.env`:
```env
CLAUDE_API_KEY=sk-ant-api03-...
GEMINI_API_KEY=AIzaSyBfaB84djM5KeIhL...
SUPABASE_URL=https://nkfrqysxrwfqqzpsjtlh.supabase.co
SUPABASE_SECRET_KEY=sb_secret_...
DYLD_LIBRARY_PATH=/opt/homebrew/lib
```

### Frontend Environment Variables
Located in `frontend/.env.local`:
```env
NEXT_PUBLIC_SUPABASE_URL=https://nkfrqysxrwfqqzpsjtlh.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_...
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📋 Testing Checklist

### ✅ Backend Tests
- [ ] `/` - Root endpoint returns status
- [ ] `/health` - Health check shows all services available
- [ ] `/docs` - Swagger docs load
- [ ] POST `/auth/signup` - User registration works
- [ ] POST `/auth/login` - User login works
- [ ] POST `/resumes/generate` - Resume generation works
- [ ] GET `/resumes/{id}/export/pdf` - PDF download works
- [ ] GET `/resumes/{id}/export/docx` - DOCX download works

### ✅ Frontend Tests
- [ ] Homepage loads at http://localhost:3000
- [ ] Navigation works
- [ ] Login/Signup forms display
- [ ] Dashboard loads after auth
- [ ] Resume generation form works
- [ ] Resume editor displays
- [ ] Truth check review shows flags
- [ ] Download buttons work

### ✅ Integration Tests
- [ ] Frontend can reach backend API
- [ ] Auth flow works end-to-end
- [ ] Resume data persists in database
- [ ] File uploads work
- [ ] PDF/DOCX downloads work from frontend

---

## 🐛 Troubleshooting

### Backend won't start
**Error:** `ModuleNotFoundError: No module named 'fastapi'`
**Fix:** Activate virtual environment first
```bash
source ../venv/bin/activate
```

**Error:** `WeasyPrint library loading errors`
**Fix:** Set library path on macOS
```bash
export DYLD_LIBRARY_PATH=/opt/homebrew/lib
```

### Frontend can't connect to backend
**Error:** `NetworkError` or `CORS error`
**Fix:** Check that:
1. Backend is running on port 8000
2. `NEXT_PUBLIC_API_URL=http://localhost:8000` in `.env.local`
3. CORS is configured in `backend/main.py` to allow `localhost:3000`

### Database connection fails
**Error:** `Supabase connection error`
**Fix:** Verify environment variables:
```bash
cd backend
python -c "from app.database import supabase; print('✅ Connected!')"
```

---

## 📊 Performance Testing

### Load Testing with curl
```bash
# Test 100 requests
for i in {1..100}; do
  curl -s http://localhost:8000/health > /dev/null
  echo "Request $i complete"
done
```

### Response Time Check
```bash
time curl http://localhost:8000/health
```

---

## 🔄 Development Workflow

1. **Make code changes**
2. **Backend auto-reloads** (if using `--reload` flag)
3. **Frontend auto-reloads** (Next.js hot reload)
4. **Test changes** in browser
5. **Run tests** to verify
6. **Commit and push** when ready

---

## 🌐 Switching to Production

When ready to test against production:

### Update Frontend Environment
```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=https://resumaker-backend-production.up.railway.app
```

### Restart Frontend
```bash
npm run dev
```

Now frontend will use production backend!

---

## 📝 Notes

- **Hot Reload:** Both frontend and backend support hot reload during development
- **Logs:** Backend logs appear in terminal, check for errors
- **Database:** Uses production Supabase database (be careful with test data!)
- **API Keys:** Uses real API keys (Claude & Gemini) - watch usage

---

## 🎯 Success Criteria

You're ready to deploy when:
- ✅ All backend tests pass
- ✅ All frontend pages load
- ✅ End-to-end user flow works
- ✅ PDF/DOCX exports download correctly
- ✅ No console errors
- ✅ Database operations succeed

---

**Last Updated:** October 7, 2025
**Status:** Backend working locally, Railway deployment in progress
