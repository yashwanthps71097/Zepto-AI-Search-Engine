# Deployment Plan: Zepto AI-powered Discovery Engine

This document provides step-by-step instructions for deploying the **Zepto AI-powered Discovery Engine** to production, hosting the static frontend dashboard on **Vercel** and the Python REST API backend on **Render** or **Railway**.

---

## 🗺️ Deployment Architecture Overview

```
┌─────────────────────────────────┐           ┌─────────────────────────────────┐
│     Frontend (Vercel CDN)       │           │    Backend Web Service          │
│                                 │           │    (Render / Railway)           │
│   dashboard/index.html          │           │   src/personalization/          │
│   dashboard/styles.css          │ ◄─────────┼   recommendation_api.py         │
│   dashboard/app.js              │  API Req  │                                 │
└─────────────────────────────────┘           └──────────────┬──────────────────┘
                                                             │ HTTPS API Call
                                                             ▼
                                                    ┌──────────────────┐
                                                    │    Groq LPU /    │
                                                    │   Pinecone DB    │
                                                    └──────────────────┘
```

---

## 🎨 1. Deploying Frontend to Vercel

Vercel is a global CDN platform perfect for serving the static files in the `/dashboard` directory.

### Step-by-Step Instructions:
1. **Prepare Repository structure:**
   Ensure your code is pushed to a Git provider (GitHub, GitLab, or Bitbucket).
2. **Sign In to Vercel:**
   Go to [Vercel](https://vercel.com/) and sign in with your GitHub account.
3. **Import Project:**
   * Click **Add New** -> **Project**.
   * Import your graduation project repository.
4. **Configure Settings (CRITICAL step to avoid build error):**
   * **Framework Preset:** Choose `Other` or `Vanilla HTML/CSS/JS`.
   * **Root Directory:** Click **Edit** and set it to **`dashboard`**. (If you leave this as the root, Vercel will see your `requirements.txt` and python files and try to compile them as serverless functions, failing with `Error: No Python entrypoint found`).
   * **Build and Development Settings:** Keep default (no build step is needed).
5. **Deploy:**
   Click **Deploy**. Once finished, Vercel will give you a public URL (e.g., `https://zepto-discovery-dashboard.vercel.app`).

> [!WARNING]
> **Troubleshooting: "No Python entrypoint found" Error**
> If you get this error during deployment, it means Vercel is looking at your root directory instead of the `/dashboard` folder. Go to **Settings** -> **General** -> scroll down to **Root Directory**, set it to `dashboard`, and click **Save**. Then trigger a new deployment.


---

## ⚡ 2. Deploying Backend to Render or Railway

Choose one of the following options to host the Python REST API server (`src/personalization/recommendation_api.py`).

### Option A: Hosting on Render (Free Tier)
1. **Create Account:** Sign in to [Render](https://render.com/) with GitHub.
2. **New Web Service:**
   * Click **New +** -> **Web Service**.
   * Select your Git repository.
3. **Configure Settings:**
   * **Name:** `zepto-discovery-api`
   * **Region:** Choose a region close to your target users (e.g., Singapore/Asia-East).
   * **Language:** `Python 3`
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `python -m src.personalization.recommendation_api`
   * **Instance Type:** `Free`
4. **Environment Variables:**
   Click the **Env** tab and add the necessary keys:
   * `PYTHONPATH` = `.`
   * `GROQ_API_KEY` = `your-actual-groq-key`
   * `PORT` = `8081` (Render automatically routes incoming traffic on port 10000 or the custom PORT variable).
5. **Deploy:** Click **Create Web Service**.

> [!NOTE]
> Render's free tier spins down (goes to sleep) after 15 minutes of inactivity. The first API request after a sleep period can take up to 50 seconds to respond.

---

### Option B: Hosting on Railway (Credit/Usage Tier)
1. **Sign In:** Go to [Railway](https://railway.app/) and sign in.
2. **New Project:**
   * Click **New Project** -> **Deploy from GitHub repo**.
   * Select your repository.
3. **Configure Variables & Start Command:**
   * Click the service card, go to **Variables**, and add:
     * `GROQ_API_KEY` = `your-actual-groq-key`
     * `PYTHONPATH` = `.`
   * Go to **Settings** -> **Deploy** -> **Start Command**: Set it to `python -m src.personalization.recommendation_api`.
4. **Expose Domain:**
   * In the service **Settings**, scroll down to **Networking** and click **Generate Domain**. Railway will create a public HTTPS endpoint (e.g., `https://zepto-discovery-api-production.up.railway.app`).

---

## 🔗 3. Connecting Frontend and Backend

Once the backend is deployed, you must update the frontend to point to the live API instead of `localhost`.

1. Open your local [dashboard/app.js](file:///c:/Users/ADMIN/Desktop/Product%20Owner/Graduation%20Project/dashboard/app.js) file.
2. Search for the local REST API calls (typically pointing to `http://localhost:8081`).
3. Replace the base URL with your new backend URL from Render/Railway:
   ```javascript
   // Before (Local development)
   const API_BASE_URL = "http://localhost:8081";

   // After (Production)
   const API_BASE_URL = "https://zepto-discovery-api.onrender.com"; 
   ```
4. Commit and push the changes to your Git repository. Vercel and your backend host will automatically detect the push and redeploy the live application!
