# Deployment Guide - TRUTH to Vercel

## Overview

Your TRUTH project has two parts:
- **Frontend** (HTML/CSS/JS) — static files, deployed to Vercel
- **Backend** (Flask + ML model) — dynamic service, needs a server (Render, Railway, or another platform)

This guide covers both deployments.

---

## Part 1: Deploy Frontend to Vercel (Fast)

### Step 1: Create Vercel Account
1. Go to [https://vercel.com](https://vercel.com)
2. Sign up with GitHub (use your GitHub account where you pushed the project)
3. Authorize Vercel to access your GitHub repositories

### Step 2: Import Your GitHub Project
1. Click **"Add New..."** → **"Project"**
2. Select your GitHub repo (look for `TRUTH` or your repo name)
3. Vercel will auto-detect that it's a Node.js/static project
4. In **Project Settings**:
   - **Build Command**: (leave blank or use) `npm run build` (not needed for static frontend)
   - **Output Directory**: `frontend`
   - **Root Directory**: `.` (or `/` — use default)
5. Click **"Deploy"** — Vercel will build and deploy your frontend

### Step 3: Note Your Frontend URL
After deployment, Vercel gives you a URL like:
```
https://your-project-name.vercel.app
```
This is your **frontend URL**. Keep it for next step.

---

## Part 2: Deploy Backend to Render (Recommended)

The Flask backend (model + analysis engine) cannot run on Vercel alone (serverless functions have size/time limits). Deploy to **Render** instead:

### Step 1: Create Render Account
1. Go to [https://render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your GitHub repos

### Step 2: Create a Web Service
1. Click **"New+"** → **"Web Service"**
2. Select your GitHub repo (`TRUTH`)
3. Fill in:
   - **Name**: `truth-backend` (or any name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**:
     ```
     gunicorn api.app:app --workers 2 --timeout 120
     ```
   - **Plan**: Free (or Paid if you need guaranteed uptime)

### Step 3: Set Environment Variables
Before deploying, add these in the **Environment** tab:
```
SECRET_KEY = your-secret-key-here (change to something random/secure)
DEBUG = False
LOG_LEVEL = INFO
FLASK_ENV = production
```

### Step 4: Deploy
Click **"Create Web Service"** — Render will:
- Pull your repo
- Install dependencies (`requirements.txt`)
- Start the Flask app
- Assign you a URL like: `https://truth-backend.onrender.com`

Keep this **backend URL** for the next step.

---

## Part 3: Connect Frontend to Backend

Your frontend (on Vercel) needs to know where the backend (on Render) is. Update the API URL:

### Option A: Using Environment Variable (Recommended)
1. In your Vercel project **Settings** → **Environment Variables**, add:
   ```
   REACT_APP_API_BASE = https://truth-backend.onrender.com/api
   ```
2. Update `frontend/static/script.js` to use:
   ```javascript
   const API_BASE = process.env.REACT_APP_API_BASE || '/api';
   ```
   (Note: Vercel doesn't support process.env in static HTML. Use the method below instead.)

### Option B: Add a Config File (Simpler for Static Frontend)
1. Create `frontend/config.js`:
   ```javascript
   // Update this URL when you deploy to a remote backend
   window.API_BASE = 'https://truth-backend.onrender.com/api'; // Replace with your Render backend URL
   ```

2. In `frontend/index.html`, add this BEFORE the closing `</body>` tag:
   ```html
   <script src="config.js"></script>
   ```

3. Redeploy frontend to Vercel (push the changes to GitHub, Vercel auto-redeploys)

### Option C: Update Frontend URL Directly in Script
Edit `frontend/static/script.js` line 3 (after you get your backend URL):
```javascript
const API_BASE = 'https://truth-backend.onrender.com/api'; // Replace with actual URL
```
Then push to GitHub and redeploy.

---

## Step 4: Test the Full System
1. Go to your Vercel frontend URL: `https://your-project-name.vercel.app`
2. Enter some news content in the "News Content" field
3. Click **"Analyze Content"**
4. Should see results from your Render backend

---

## Troubleshooting

### "Analysis failed: Failed to fetch"
- Frontend can't reach backend. Check:
  1. Backend URL in `script.js` is correct
  2. Backend is running (check Render dashboard)
  3. CORS is enabled in Flask (it is — `CORS(app)` is in `api/app.py`)

### Model File Error ("File is not a zip file")
- The corrupted model file (`models/fake_news_detector.pkl`) is being loaded
- Fix: Delete the `.pkl` file from your repo (it's already in `.gitignore`) before deploying
- The system will fall back to default behavior

### 502/503 Errors on Render
- Backend crashed or is starting up. Check Render logs:
  - Render dashboard → your service → **Logs** tab
- Common issues:
  - Missing dependencies in `requirements.txt`
  - NLTK data missing (handled in `api/app.py` — should auto-download)
  - Model file issues

### Frontend Loads But No Results
- Check browser console (F12 → Console tab) for error messages
- Verify the API_BASE URL is correct and points to your Render backend

---

## Summary of URLs

After deployment, you have:

| Component | Platform | URL |
|-----------|----------|-----|
| Frontend | Vercel | `https://your-project-name.vercel.app` |
| Backend | Render | `https://truth-backend.onrender.com` (replace with actual) |

Your users visit the **Vercel frontend URL** and it calls the **Render backend API**.

---

## Optional: Custom Domain
- **Vercel**: Add custom domain in Project Settings → Domains
- **Render**: Add custom domain in Service Settings → Custom Domain

---

## Costs
- **Vercel**: Free tier covers frontend hosting
- **Render**: Free tier covers backend (with 15-minute auto-shutdown on inactivity). Upgrade to Paid for always-on service.

---

## Next Steps
1. Push your repo to GitHub (if not done)
2. Deploy frontend to Vercel (Part 1 above)
3. Deploy backend to Render (Part 2 above)
4. Connect them (Part 3 above)
5. Test at `https://your-vercel-url`

Good luck! 🚀
