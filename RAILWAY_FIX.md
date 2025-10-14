# Railway Deployment Fix - "Could not find root directory: backend"

## The Problem:
Railway can't find your `backend` folder because the service isn't properly linked to GitHub.

## The Solution (Web UI - 2 minutes):

### Step 1: Delete the Broken Service (if it exists)
1. In Railway, look for any service cards/boxes
2. Click the three dots menu → Delete service
3. Confirm deletion

### Step 2: Create New Service from GitHub
1. Click the "+ New" button in Railway (top right usually)
2. Select "Deploy from GitHub repo"
3. Choose: `username-ebro/resumaker`
4. **IMPORTANT:** Set "Root Directory" to `backend` (type it in the field)
5. Railway will auto-detect it's a Python app

### Step 3: Add Environment Variables
Before deploying, add these variables (click "Add Variables"):

```
ANTHROPIC_API_KEY=<your_anthropic_key>
GEMINI_API_KEY=<your_gemini_key>
SUPABASE_URL=https://nkfrqysxrwfqqzpsjtlh.supabase.co
SUPABASE_KEY=<your_supabase_service_role_key>
SUPABASE_JWT_SECRET=<your_jwt_secret>
DATABASE_URL=postgresql://postgres:<password>@db.nkfrqysxrwfqqzpsjtlh.supabase.co:5432/postgres
PORT=8000
```

### Step 4: Deploy
1. Click "Deploy"
2. Wait 2-3 minutes for build
3. Click "Settings" → "Generate Domain"
4. Copy the URL and give it to me

---

## OR - Simpler Alternative:

Since Railway is being tricky, let's just keep using ngrok for now!

Your app is ALREADY LIVE and working:
https://resumaker-jgudtuoq4-evan-1154s-projects.vercel.app

Your friend can test it right now. The ngrok tunnel works perfectly for demos.

---

## What Do You Prefer?

1. **Fix Railway** (permanent, but requires setup)
2. **Keep ngrok** (works now, 2-hour limit but auto-restart script ready)
3. **Deploy to Render.com instead** (easier than Railway, also free tier)

Your call!
