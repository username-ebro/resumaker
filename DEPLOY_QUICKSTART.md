# 🚀 Deploy Resumaker - 5 Minute Guide

**Goal:** Get the app live so your friend can test it

**Architecture:**
- Backend (Python/FastAPI) → Railway
- Frontend (Next.js) → Vercel
- Database (PostgreSQL) → Supabase (already live ✅)

---

## Step 1: Deploy Backend to Railway (2 min)

### Option A: Railway CLI (Fastest)
```bash
cd backend

# Login to Railway (opens browser)
railway login

# Link to existing project OR create new one
railway link  # If you have existing project
# OR
railway init  # To create new project

# Deploy!
railway up

# Get your backend URL
railway domain
# Example output: https://resumaker-backend-production.up.railway.app
```

### Option B: Railway Web UI
1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Connect your GitHub account
4. Select the `resumaker` repo
5. Root Directory: `/backend`
6. Railway will auto-detect Python and use `nixpacks.toml`
7. Wait 2-3 minutes for build
8. Click "Settings" → "Generate Domain" to get public URL

### Set Environment Variables in Railway:
```
ANTHROPIC_API_KEY=<your_key>
GEMINI_API_KEY=<your_key>
SUPABASE_URL=https://nkfrqysxrwfqqzpsjtlh.supabase.co
SUPABASE_KEY=<your_supabase_key>
SUPABASE_JWT_SECRET=<your_jwt_secret>
DATABASE_URL=<your_supabase_postgres_url>
```

**Get your Railway URL:** Copy it! You'll need it for Step 2.

---

## Step 2: Update Frontend API URL (30 sec)

```bash
cd frontend

# Edit .env.local
# Change this line:
NEXT_PUBLIC_API_URL=http://localhost:8000

# To your Railway URL:
NEXT_PUBLIC_API_URL=https://resumaker-backend-production.up.railway.app
```

---

## Step 3: Deploy Frontend to Vercel (2 min)

### Option A: Vercel CLI (Fastest)
```bash
cd frontend

# Install Vercel CLI if needed
npm i -g vercel

# Login
vercel login

# Deploy!
vercel --prod

# Vercel will give you a URL like:
# https://resumaker-yourusername.vercel.app
```

### Option B: Vercel Web UI
1. Go to https://vercel.com/new
2. Import your GitHub repo
3. Root Directory: `/frontend`
4. Framework: Next.js (auto-detected)
5. Add Environment Variables:
   ```
   NEXT_PUBLIC_API_URL=<your_railway_url>
   NEXT_PUBLIC_SUPABASE_URL=https://nkfrqysxrwfqqzpsjtlh.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_c2jaFL882bD4wv3hcN9e8w_GScQSy8b
   ```
6. Click "Deploy"

---

## Step 4: Share with Friend! 🎉

Send them the Vercel URL:
```
Hey! Check out Resumaker: https://resumaker-yourusername.vercel.app

Try:
1. Sign up for an account
2. Upload a resume (PDF/DOCX)
3. Or have a conversation to build your knowledge base
4. Generate a job-specific resume
```

---

## Quick Troubleshooting

### Backend won't start on Railway:
- Check logs: `railway logs` or in Railway dashboard
- Verify all environment variables are set
- WeasyPrint dependencies in `nixpacks.toml` should auto-install

### Frontend can't connect to backend:
- Check `NEXT_PUBLIC_API_URL` in Vercel environment variables
- Must be HTTPS (Railway provides this automatically)
- Check browser console for CORS errors

### "Database connection failed":
- Verify Supabase credentials in Railway
- Check that `DATABASE_URL` includes password

---

## One-Line Deploy (If you have CLIs installed)

```bash
# Backend
cd backend && railway up && railway domain

# Frontend (after updating NEXT_PUBLIC_API_URL)
cd ../frontend && vercel --prod
```

---

## Cost Breakdown

| Service | Free Tier | Our Usage | Cost |
|---------|-----------|-----------|------|
| Railway | $5 credit/month | ~$2-3/month | $0-3/month |
| Vercel | 100GB bandwidth | <10GB | $0 |
| Supabase | 500MB DB, 2GB bandwidth | <100MB | $0 |
| **TOTAL** | | | **~$0-3/month** |

---

## Already Configured ✅

- ✅ `backend/railway.json` - Railway deployment config
- ✅ `backend/nixpacks.toml` - WeasyPrint dependencies
- ✅ `backend/Procfile` - Start command
- ✅ `backend/requirements.txt` - Python dependencies
- ✅ `frontend/vercel.json` - Vercel config
- ✅ Database migrations - Already run on Supabase
- ✅ CORS - FastAPI configured for cross-origin requests

---

## For Continuous Deployment (Optional)

Both Railway and Vercel support auto-deploy from GitHub:

1. Push your code to GitHub
2. Connect Railway to your repo (Settings → Deploy Triggers)
3. Connect Vercel to your repo (Settings → Git Integration)
4. Every `git push` auto-deploys! 🚀

---

## Alternative: Super Quick Test (Tunnel Local Backend)

If you just want to test RIGHT NOW without deploying:

```bash
# Install ngrok
brew install ngrok  # or download from ngrok.com

# In terminal 1: Start backend
cd backend && python3 main.py

# In terminal 2: Tunnel it
ngrok http 8000
# Copy the HTTPS URL: https://abc123.ngrok.io

# Update frontend/.env.local
NEXT_PUBLIC_API_URL=https://abc123.ngrok.io

# In terminal 3: Deploy frontend only
cd frontend && vercel --prod
```

**Note:** ngrok URLs expire after 2 hours on free plan

---

**Ready to deploy?** Start with Step 1! Takes ~5 minutes total.
