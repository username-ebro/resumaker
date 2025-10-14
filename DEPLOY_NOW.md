# 🚀 Deploy Resumaker RIGHT NOW

**Everything is ready!** Code is pushed to GitHub. Just follow these steps:

---

## Step 1: Deploy Backend to Railway (2 minutes)

### Click this link:
👉 **https://railway.app/new/github**

1. **Select repository:** `username-ebro/resumaker`
2. **Root Directory:** Type `backend` in the "Root Directory" field
3. **Add Environment Variables:** Click "Add Variables" and paste this:

```
ANTHROPIC_API_KEY=your_anthropic_key_here
GEMINI_API_KEY=your_gemini_key_here
SUPABASE_URL=https://nkfrqysxrwfqqzpsjtlh.supabase.co
SUPABASE_KEY=your_supabase_service_role_key
SUPABASE_JWT_SECRET=your_jwt_secret
DATABASE_URL=postgresql://postgres:your_password@db.nkfrqysxrwfqqzpsjtlh.supabase.co:5432/postgres
```

4. **Click "Deploy"**
5. **Wait 2-3 minutes for build**
6. **Click "Settings" → "Generate Domain"**
7. **Copy the URL** (looks like: `https://resumaker-backend-production-abc123.up.railway.app`)

---

## Step 2: Deploy Frontend to Vercel (AUTOMATED)

I'll do this for you once you give me the Railway URL from Step 1.

Just paste the Railway URL here and I'll:
1. Update the frontend environment variable
2. Deploy to Vercel
3. Give you the live URL to share with your friend

---

## What I need from you:

1. **Railway backend URL** (from Step 1 above)
2. **Your API keys** (if you want me to add them to Railway, or you can do it manually)

---

## OR: I can create a simpler test deployment

If you want to skip Railway for now, I can:
1. Deploy ONLY the frontend to Vercel
2. Use your local backend via ngrok tunnel (2-hour temporary link)
3. Your friend can test it immediately

Which would you prefer?

---

**Status:** ✅ Code pushed to GitHub (commit 92e8171)
**Ready for:** Railway deployment (needs your API keys)
