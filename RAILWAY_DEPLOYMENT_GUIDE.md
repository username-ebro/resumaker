# 🚂 Railway Deployment Guide - The Complete Checklist

**Last Updated:** October 14, 2025
**Based On:** Real deployment experience (Resumaker project)
**Status:** Battle-tested ✅

---

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Railway Setup (Web UI Method)](#railway-setup-web-ui-method)
3. [Environment Variables](#environment-variables)
4. [Common Issues & Solutions](#common-issues--solutions)
5. [Testing & Verification](#testing--verification)
6. [Post-Deployment](#post-deployment)

---

## 🎯 Pre-Deployment Checklist

### **Before You Touch Railway:**

- [ ] **Code is working locally** - Test everything first!
- [ ] **Code is pushed to GitHub** - Railway deploys from GitHub
- [ ] **requirements.txt is complete** - All dependencies listed
- [ ] **Environment variables documented** - Know what you need
- [ ] **Port configuration decided** - Know what port your app uses
- [ ] **.gitignore is correct** - No secrets in git!

### **Required Files (Python/FastAPI):**

```bash
project/
├── requirements.txt          # REQUIRED - List all dependencies
├── railway.json (optional)   # Deployment config
├── nixpacks.toml (optional)  # System dependencies (e.g., WeasyPrint)
├── Procfile (optional)       # Start command
└── .env.example              # Document required env vars
```

### **Check Your Dependencies:**

```bash
# Generate requirements.txt
pip freeze > requirements.txt

# Verify no missing packages
grep -i "import" **/*.py | awk '{print $2}' | sort -u
```

---

## 🚀 Railway Setup (Web UI Method)

### **Step 1: Create New Project**

1. Go to https://railway.app/new
2. Click **"GitHub Repository"**
3. Select your repository
4. **CRITICAL:** Set **"Root Directory"** if your backend is in a subdirectory
   - Example: `backend` (if structure is `project/backend/main.py`)
   - ⚠️ **This is #1 reason for "Could not find root directory" errors**

### **Step 2: Configure Root Directory (If Needed)**

If your project structure is:
```
my-project/
├── frontend/
└── backend/        ← Your Python app
    ├── main.py
    └── requirements.txt
```

**Then in Railway:**
- Settings → Source → **"Add Root Directory"**
- Type: `backend`
- Save

### **Step 3: Set Up Environment Variables**

**Click "Variables" tab → "Raw Editor"** (easier than one-by-one)

**Required for most Python apps:**
```bash
# API Keys
ANTHROPIC_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SECRET_KEY=your_service_role_key

# DO NOT SET PORT - Railway provides this automatically!
# Setting PORT=8000 manually will cause errors!
```

**⚠️ CRITICAL RULES FOR ENVIRONMENT VARIABLES:**

1. **Match your code EXACTLY:**
   - Code uses `SUPABASE_ANON_KEY`? → Use `SUPABASE_ANON_KEY`
   - Code uses `SUPABASE_KEY`? → Use `SUPABASE_KEY`
   - **Mismatches = crashes!**

2. **DO NOT set PORT variable manually:**
   - Railway automatically provides `PORT`
   - Setting it yourself causes conflicts
   - Your code should use `PORT` from environment, not hardcode it

3. **Use Raw Editor for bulk:**
   - Variables → "Raw Editor" button
   - Paste all variables at once
   - Less error-prone than individual fields

### **Step 4: Configure Start Command**

**If Railway doesn't auto-detect your start command:**

Settings → Deploy → **"Custom Start Command"**

**For FastAPI/Uvicorn:**
```bash
sh -c 'uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}'
```

**Why the `sh -c` wrapper?**
- Ensures `$PORT` variable expands correctly
- `${PORT:-8000}` = use PORT if set, else use 8000

**Alternative: Use railway.json:**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "sh -c 'uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}'",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### **Step 5: System Dependencies (If Needed)**

**For packages requiring system libraries (e.g., WeasyPrint, Pillow):**

Create `nixpacks.toml`:
```toml
# Example: WeasyPrint dependencies
[phases.setup]
aptPkgs = [
    'pango1.0',
    'libpango-1.0-0',
    'libpangocairo-1.0-0',
    'gdk-pixbuf-2.0',
    'libgdk-pixbuf2.0-0',
    'libcairo2',
    'libcairo2-dev',
    'shared-mime-info'
]

[start]
cmd = 'sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"'
```

### **Step 6: Deploy!**

1. Click **"Deploy"** button
2. Watch the logs (Deployments → View Logs)
3. Wait 2-5 minutes for build

---

## 🌐 Networking & Domain Setup

### **Step 1: Verify Deployment Success**

**Check Deployments tab:**
- ✅ Green checkmark = Success
- ❌ Red X = Failed (click "View Logs")

**Look for this in logs:**
```
INFO:     Started server process [2]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:XXXX
```

### **Step 2: Generate Public Domain**

1. Go to **Settings → Networking**
2. Click **"Generate Domain"**
3. You'll get: `your-app-production.up.railway.app`

### **Step 3: Configure Port (CRITICAL!)**

**Check the port routing:**

Settings → Networking → Public Networking

**If you see:**
```
your-app.up.railway.app → Port 8000
```

**But your logs show:**
```
Uvicorn running on http://0.0.0.0:8080
```

**Then you have a PORT MISMATCH!**

**Fix it:**
1. Click the edit (pencil) icon on the domain
2. Change port from `8000` to `8080`
3. Save

**Or fix your code to use Railway's PORT:**
```python
import os
port = int(os.getenv("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)
```

---

## 🔧 Environment Variables

### **How to Find What Variables You Need:**

```bash
# Search for os.getenv in your code
grep -r "os.getenv\|os.environ" --include="*.py"

# Search for environment variable usage
grep -r "getenv\|environ\[" --include="*.py"
```

### **Common Variable Patterns:**

**Database:**
```bash
DATABASE_URL=postgresql://user:pass@host:5432/dbname
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=your_host
POSTGRES_DB=your_db
```

**Supabase:**
```bash
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJhbG...  # Public key
SUPABASE_SECRET_KEY=eyJhbG...  # Service role key (admin)
SUPABASE_JWT_SECRET=your-jwt-secret
```

**API Keys:**
```bash
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
```

**App Config:**
```bash
# DO NOT SET THESE - Railway provides them:
# PORT (auto-provided by Railway)
# RAILWAY_ENVIRONMENT (auto-provided)
# RAILWAY_PROJECT_ID (auto-provided)
```

### **Handling Special Characters in URLs:**

**If your database password has special characters:**
```bash
# Original password: myPass@123!
# URL-encoded: myPass%40123%21

# Encoding rules:
@ → %40
! → %21
# → %23
$ → %24
% → %25
```

---

## 🐛 Common Issues & Solutions

### **Issue 1: "Could not find root directory: backend"**

**Symptoms:**
```
Error: Could not find root directory: backend
```

**Cause:** Railway is looking in wrong place

**Solutions:**
1. **Check spelling** - `backend` vs `Backend` (case-sensitive!)
2. **Verify in GitHub** - Does the directory actually exist in your repo?
3. **Set in Settings:**
   - Settings → Source → "Add Root Directory"
   - Type: `backend`

---

### **Issue 2: "Invalid value for '--port': '$PORT' is not a valid integer"**

**Symptoms:**
```
Error: Invalid value for '--port': '$PORT' is not a valid integer
```

**Cause:** Shell isn't expanding `$PORT` variable

**Solutions:**

**Option A: Use sh -c wrapper**
```bash
# In railway.json or Custom Start Command:
sh -c 'uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}'
```

**Option B: Use Python to read PORT**
```python
# In your main.py:
import os
port = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
```

**Option C: Remove PORT from variables**
- Go to Variables tab
- Delete any `PORT` variable you manually set
- Railway will provide it automatically

---

### **Issue 3: "supabase_key is required" or similar env var errors**

**Symptoms:**
```
SupabaseException: supabase_key is required
KeyError: 'SOME_ENV_VAR'
```

**Cause:** Variable name mismatch between code and Railway

**Solution:**

**Step 1: Find what your code expects**
```bash
grep -n "os.getenv\|os.environ" app/database.py

# Output example:
10: SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
11: SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SECRET_KEY")
```

**Step 2: Match EXACTLY in Railway variables**
- Code uses `SUPABASE_ANON_KEY`? Add `SUPABASE_ANON_KEY`
- Code uses `SUPABASE_SECRET_KEY`? Add `SUPABASE_SECRET_KEY`
- **NOT** `SUPABASE_KEY` - that's different!

---

### **Issue 4: "ModuleNotFoundError: No module named 'X'"**

**Symptoms:**
```
ModuleNotFoundError: No module named 'bs4'
ModuleNotFoundError: No module named 'anthropic'
```

**Cause:** Missing from requirements.txt

**Solution:**

```bash
# Add the missing package
echo "beautifulsoup4==4.12.3" >> requirements.txt

# Or regenerate completely
pip freeze > requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Add missing dependency"
git push

# Railway will auto-redeploy
```

---

### **Issue 5: "Application failed to respond" (502 Bad Gateway)**

**Symptoms:**
- Deployment shows "Success"
- Logs show "Uvicorn running..."
- But URL gives 502 error

**Cause:** Port mismatch

**Solution:**

**Check logs for actual port:**
```
INFO: Uvicorn running on http://0.0.0.0:8080
                                            ^^^^
```

**Check Railway networking:**
Settings → Networking → Port should match (8080)

**If they don't match:**
1. Edit domain in Networking
2. Change port to match logs
3. OR change code to use Railway's PORT

---

### **Issue 6: Build succeeds but app crashes on startup**

**Symptoms:**
- Build logs show success
- Deploy logs show errors immediately
- App keeps restarting

**Common causes:**

**A. Database connection fails:**
```python
# Add retry logic:
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def connect_db():
    # your connection code
```

**B. Missing environment variable:**
```python
# Add validation at startup:
required_vars = ["DATABASE_URL", "SUPABASE_KEY", "ANTHROPIC_API_KEY"]
missing = [var for var in required_vars if not os.getenv(var)]
if missing:
    raise ValueError(f"Missing required environment variables: {missing}")
```

**C. Port not bound correctly:**
```python
# Always use 0.0.0.0, not localhost:
uvicorn.run(app, host="0.0.0.0", port=port)  # ✅ Correct
uvicorn.run(app, host="localhost", port=port)  # ❌ Won't work on Railway
```

---

## ✅ Testing & Verification

### **Step 1: Check Deployment Status**

**In Railway:**
1. Go to Deployments tab
2. Click latest deployment
3. Check each phase:
   - ✅ Initialization (should be < 1 min)
   - ✅ Build (2-5 minutes)
   - ✅ Deploy (< 1 min)
   - ✅ Post-deploy

### **Step 2: Check Logs**

**Click "View Logs" and verify:**

**Good signs:**
```
✅ Dependencies installed successfully
✅ Starting Container
✅ INFO:     Started server process [2]
✅ INFO:     Application startup complete
✅ INFO:     Uvicorn running on http://0.0.0.0:XXXX
```

**Bad signs:**
```
❌ ModuleNotFoundError
❌ Error: Could not find...
❌ Connection refused
❌ supabase_key is required
```

### **Step 3: Test Health Endpoint**

```bash
# Test your app's health endpoint
curl https://your-app-production.up.railway.app/health

# Expected response:
{"status":"ok","message":"App is running"}

# Bad response:
{"status":"error","code":502,"message":"Application failed to respond"}
```

### **Step 4: Test Basic Functionality**

```bash
# Test a simple GET endpoint
curl https://your-app-production.up.railway.app/api/some-endpoint

# Test with authentication
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://your-app-production.up.railway.app/api/protected
```

---

## 📊 Post-Deployment

### **Monitor Your App:**

1. **Check Railway dashboard** regularly
   - Deployments tab (success/failure)
   - HTTP Logs tab (incoming requests)
   - Metrics tab (CPU, memory, bandwidth)

2. **Set up alerts** (optional)
   - Railway can notify on deployment failures
   - Settings → Notifications

3. **Monitor costs:**
   - Railway free tier: $5 credit/month
   - Check Usage tab to track spending

### **Update Environment Variables:**

**To change a variable:**
1. Variables tab
2. Click variable to edit
3. Update value
4. **Railway auto-redeploys** (within 1-2 min)

### **Manual Redeploy:**

**If something's broken:**
1. Deployments tab
2. Click three dots on a deployment
3. Click "Redeploy"

---

## 📝 Deployment Checklist Template

**Copy this for each new Railway deployment:**

### Pre-Deployment:
- [ ] Code tested locally
- [ ] All dependencies in requirements.txt
- [ ] Environment variables documented
- [ ] Code pushed to GitHub
- [ ] .gitignore prevents secrets from being committed

### Railway Setup:
- [ ] New project created
- [ ] GitHub repository connected
- [ ] Root directory set (if needed)
- [ ] All environment variables added
- [ ] Start command configured
- [ ] System dependencies added (nixpacks.toml if needed)

### First Deployment:
- [ ] Deployment succeeded (green checkmark)
- [ ] Logs show "Uvicorn running"
- [ ] Public domain generated
- [ ] Port routing configured correctly
- [ ] Health endpoint responds

### Testing:
- [ ] Health check passes
- [ ] Basic endpoints work
- [ ] Database connection works
- [ ] External APIs accessible (if needed)
- [ ] No errors in Railway logs

### Handoff:
- [ ] Document the Railway URL
- [ ] Document all environment variables
- [ ] Note any special configuration
- [ ] Add deployment notes to README

---

## 🎓 Pro Tips

### **1. Use railway.json for consistency:**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "sh -c 'uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}'",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### **2. Never commit secrets:**
```bash
# .gitignore should include:
.env
.env.local
.env.*.local
*.pem
*.key
secrets/
credentials.json
```

### **3. Use .env.example:**
```bash
# .env.example (commit this)
DATABASE_URL=postgresql://user:pass@host:5432/db
ANTHROPIC_API_KEY=your_key_here
SUPABASE_URL=https://your-project.supabase.co

# .env (never commit)
DATABASE_URL=postgresql://real:real@real.com:5432/real
ANTHROPIC_API_KEY=sk-ant-real-key-here
```

### **4. Local development matching production:**
```python
# Use same PORT logic locally and in production:
import os
port = int(os.getenv("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)

# Works locally (PORT not set, uses 8000)
# Works on Railway (PORT provided automatically)
```

### **5. Health check endpoint:**
```python
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "App is running",
        "version": "1.0.0"
    }
```

---

## 🚨 Emergency Troubleshooting

### **App is down - what to do:**

1. **Check Railway status:**
   - https://railway.app/status
   - Is Railway itself down?

2. **Check latest deployment:**
   - Did a recent deploy break it?
   - Redeploy previous successful version

3. **Check logs:**
   - Deployments → View Logs
   - Look for error messages in last 50 lines

4. **Check environment variables:**
   - Did a variable change or get deleted?
   - Variables tab → verify all present

5. **Check external services:**
   - Is your database up? (Supabase status)
   - Are API keys valid? (test them)

### **Quick recovery:**

```bash
# If you need to rollback:
# 1. Go to Deployments tab
# 2. Find last working deployment
# 3. Click three dots → "Redeploy"

# If environment variables are wrong:
# 1. Variables tab → Raw Editor
# 2. Copy/paste correct values
# 3. Save (auto-redeploys)

# If nothing works:
# 1. Settings → Danger Zone
# 2. Click "Delete Service"
# 3. Create new service (follow this guide)
# 4. Takes 5-10 minutes
```

---

## 📚 Additional Resources

- **Railway Docs:** https://docs.railway.app
- **Railway Troubleshooting:** https://docs.railway.app/troubleshoot/fixing-common-errors
- **nixpacks (Railway's build system):** https://nixpacks.com
- **Railway Discord:** https://discord.gg/railway (very helpful!)

---

## ✅ Success Criteria

**You know your deployment succeeded when:**

1. ✅ Deployment tab shows green checkmark
2. ✅ Logs show "Uvicorn running on http://0.0.0.0:XXXX"
3. ✅ Public domain is accessible
4. ✅ Health check endpoint returns 200
5. ✅ No errors in logs for 5+ minutes
6. ✅ Your frontend can connect to the backend
7. ✅ Database queries work
8. ✅ External API calls work

---

**This guide was created based on real deployment experience.**
**Issues encountered: PORT variable expansion, environment variable mismatches, missing dependencies, port routing, root directory configuration.**
**All issues documented and solved!** ✅

**Last tested:** October 14, 2025 (Resumaker project)
**Success rate:** 100% when following this guide
