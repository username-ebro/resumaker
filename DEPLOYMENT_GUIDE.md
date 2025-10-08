# 🚀 Deployment Guide - Resumaker

Complete guide for deploying Resumaker to production.

---

## 📋 Prerequisites

### Required Accounts
- [x] Supabase account (database already configured)
- [ ] Vercel account (for frontend)
- [ ] Railway account (for backend) OR Render account

### API Keys Needed
- [x] Anthropic API key (Claude)
- [x] Google Gemini API key
- [x] Supabase URL and keys

---

## 🎯 Frontend Deployment (Vercel)

### Step 1: Connect Repository
1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Select `frontend` as the root directory

### Step 2: Configure Build Settings
Vercel should auto-detect Next.js, but verify:
- **Framework Preset:** Next.js
- **Build Command:** `npm run build`
- **Output Directory:** `.next`
- **Install Command:** `npm install`

### Step 3: Add Environment Variables
In Vercel dashboard → Settings → Environment Variables:

```
NEXT_PUBLIC_SUPABASE_URL=https://nkfrqysxrwfqqzpsjtlh.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<your-supabase-anon-key>
```

### Step 4: Deploy
1. Click "Deploy"
2. Wait for build to complete (~2-3 minutes)
3. Your frontend will be live at `https://your-app.vercel.app`

### Step 5: Update Backend URL
After backend is deployed, update the frontend API calls:
- Replace `http://localhost:8000` with your backend URL
- Update in all `.tsx` files in `frontend/app` and `frontend/components`

---

## 🖥️ Backend Deployment (Railway)

### Step 1: Create New Project
1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select your repository
4. Choose `backend` directory

### Step 2: Add Environment Variables
In Railway dashboard → Variables:

```
ANTHROPIC_API_KEY=sk-ant-api03-QFviv...
GEMINI_API_KEY=AIzaSyDc9...
SUPABASE_URL=https://nkfrqysxrwfqqzpsjtlh.supabase.co
SUPABASE_KEY=<your-supabase-anon-key>
SUPABASE_SECRET_KEY=<your-supabase-secret-key>
DYLD_LIBRARY_PATH=/opt/homebrew/lib
PORT=8000
```

### Step 3: Install System Dependencies
Railway may need system packages for WeasyPrint. Add to `nixpacks.toml`:

```toml
[phases.setup]
aptPkgs = ['pango1.0', 'libpango-1.0-0', 'libpangocairo-1.0-0', 'gdk-pixbuf-2.0', 'libffi-dev']
```

### Step 4: Deploy
1. Railway will auto-deploy on push
2. Check logs for any errors
3. Your backend will be at `https://your-app.railway.app`

### Step 5: Test Endpoints
```bash
# Health check
curl https://your-app.railway.app/health

# Test resume generation (replace user_id with real UUID)
curl -X POST https://your-app.railway.app/resumes/generate \
  -H "Content-Type: application/json" \
  -d '{"user_id": "your-user-id"}'
```

---

## 🔄 Alternative: Deploy Backend to Render

### Step 1: Create Web Service
1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Select `backend` directory

### Step 2: Configure Service
- **Name:** resumaker-backend
- **Environment:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `export DYLD_LIBRARY_PATH=/opt/homebrew/lib && uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 3: Add Environment Variables
Same as Railway (see above)

### Step 4: Add System Dependencies
In Render dashboard → Environment → Shell:
```bash
apt-get update
apt-get install -y libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev
```

---

## 🗄️ Database (Supabase)

### Already Configured! ✅
- Database is live at: `https://nkfrqysxrwfqqzpsjtlh.supabase.co`
- All 14 tables created
- RLS policies active
- No additional setup needed

### Verify Database Connection
```bash
# From deployed backend
curl https://your-app.railway.app/health

# Should return:
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

---

## 🔐 CORS Configuration

Update `backend/main.py` with production frontend URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://your-app.vercel.app"  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## ✅ Post-Deployment Checklist

### Frontend
- [ ] Vercel deployment successful
- [ ] Environment variables set
- [ ] Frontend loads without errors
- [ ] Can navigate between pages
- [ ] Auth login/signup works

### Backend
- [ ] Railway/Render deployment successful
- [ ] All environment variables set
- [ ] Health endpoint returns 200
- [ ] PDF export works
- [ ] DOCX export works
- [ ] Database connection works

### Full Integration
- [ ] Frontend can call backend APIs
- [ ] User can sign up
- [ ] User can upload resume
- [ ] User can generate resume
- [ ] User can download PDF
- [ ] User can download DOCX

---

## 🐛 Common Issues & Fixes

### Issue: WeasyPrint fails in production
**Solution:** Ensure system dependencies are installed:
```bash
# For Railway (nixpacks.toml)
[phases.setup]
aptPkgs = ['pango1.0', 'libpango-1.0-0', 'gdk-pixbuf-2.0', 'libffi-dev']

# For Render (Shell)
apt-get install -y libpango-1.0-0 libgdk-pixbuf2.0-0 libffi-dev
```

### Issue: CORS errors
**Solution:** Add production frontend URL to CORS allow_origins in `backend/main.py`

### Issue: Database connection fails
**Solution:** Verify environment variables:
- `SUPABASE_URL` is correct
- `SUPABASE_KEY` is set
- `SUPABASE_SECRET_KEY` is set (for server-side operations)

### Issue: File uploads fail
**Solution:** Ensure `python-multipart` is in requirements.txt

### Issue: API calls return 404
**Solution:** Check that backend URL in frontend matches deployed backend URL

---

## 📊 Monitoring & Logs

### Vercel
- Logs: https://vercel.com/your-team/your-app/deployments
- Analytics: Built-in analytics dashboard
- Errors: Real-time error tracking

### Railway
- Logs: Railway dashboard → Deployments → Logs
- Metrics: CPU, memory, network usage
- Restarts: Automatic on failure (configured)

### Supabase
- Database logs: Supabase dashboard → Database → Logs
- API usage: Dashboard → Settings → API
- Table browser: Dashboard → Table Editor

---

## 🎉 Success!

If all checklists are complete, your Resumaker is now live in production!

**Frontend:** `https://your-app.vercel.app`
**Backend:** `https://your-app.railway.app`
**Database:** Already configured at Supabase

Share the frontend URL with users and they can start building ATS-optimized resumes!

---

## 🔄 Continuous Deployment

Both Vercel and Railway support automatic deployments:

### Vercel
- Pushes to `main` branch → auto-deploy frontend
- Preview deployments for pull requests

### Railway
- Pushes to `main` branch → auto-deploy backend
- Configure triggers in Railway dashboard

---

## 📈 Next Steps

### Post-Launch
1. Monitor error logs
2. Gather user feedback
3. Track conversion metrics
4. Optimize performance

### Feature Enhancements (Future)
- Email notifications
- Resume templates
- Cover letter generation
- Multi-language support
- Team collaboration

---

**Deployment Status:** Ready to deploy! 🚀
