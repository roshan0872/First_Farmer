# First Farmer Agriculture System &mdash; Deployment Guide

## GitHub &rarr; Neon Postgres &rarr; Vercel Serverless

This guide outlines the complete steps to deploy **First Farmer Agriculture System** to Vercel using a serverless Neon PostgreSQL database.

---

## 1. Prerequisites
- A free account on [GitHub](https://github.com)
- A free account on [Neon](https://neon.tech)
- A free account on [Vercel](https://vercel.com)
- Python 3.11+ installed on your developer machine

---

## 2. Step 1: Create a Neon Postgres Database
1. Log into your [Neon Console](https://console.neon.tech).
2. Create a new project named `first-farmer-db`.
3. In the project dashboard, locate the **Connection Details** section.
4. Select **Pooled connection** and choose the **SQLAlchemy** or **Python** format.
   The connection string will resemble:
   ```
   postgresql://user:password@ep-xyz-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
5. Note: Our application's `normalize_database_url` automatically adapts `postgres://` or `postgresql://` into `postgresql+psycopg://` and guarantees `sslmode=require` is appended.

---

## 3. Step 2: Initialize & Seed Neon from Developer Machine
Because serverless functions on Vercel have an ephemeral, read-only filesystem and strict execution timeouts, **database schema migrations and content seeding never run at request time**. They are executed once from your local developer machine directly against the Neon database:

### Windows (PowerShell):
```powershell
# Set Neon DATABASE_URL in your active terminal session
$env:DATABASE_URL="postgresql+psycopg://user:password@ep-xyz-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

# Run database seeder with content only (no dev demo users)
.\.venv\Scripts\python seed\seed.py --content-only

# Create your production administrator account securely
.\.venv\Scripts\python -m flask create-admin
```

### macOS / Linux:
```bash
export DATABASE_URL="postgresql+psycopg://user:password@ep-xyz-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

python seed/seed.py --content-only
flask create-admin
```

---

## 4. Step 3: Push Repository to GitHub
Ensure `.env` and `instance/*.db` files are ignored by git (verified in `.gitignore`):
```bash
git add .
git commit -m "Complete First Farmer Agriculture System production build"
git branch -M main
git remote add origin https://github.com/your-username/first-farmer-agriculture-system.git
git push -u origin main
```

---

## 5. Step 4: Import into Vercel & Set Environment Variables
1. Go to your [Vercel Dashboard](https://vercel.com/dashboard) and click **Add New... &rarr; Project**.
2. Select your GitHub repository `first-farmer-agriculture-system`.
3. Under **Environment Variables**, add the following keys:

| Key | Value | Description |
|---|---|---|
| `APP_ENV` | `production` | Enables production security mode and enforces strict cookies |
| `SECRET_KEY` | *(generate a 32+ character random secret)* | Required in production (app refuses to start with default) |
| `DATABASE_URL` | `postgresql+psycopg://user:password@ep-xyz-pooler...` | Your pooled Neon Postgres connection string |
| `WEATHER_API_KEY` | *(optional)* | OpenWeatherMap API key for live weather observations |
| `AI_PROVIDER` | *(optional)* | AI provider name if configuring external grounding model |
| `AI_API_KEY` | *(optional)* | API key for AI provider |

4. Click **Deploy**. Vercel will install dependencies from `requirements.txt` and launch the WSGI handler defined in `app.py`.

---

## 6. Step 5: Post-Deployment Verification
1. **Health Check**: Open `https://your-app.vercel.app/healthz`. Confirm it returns HTTP 200 with `{"status": "healthy", "database": "connected"}`.
2. **User Registration**: Register a new student account at `/register`.
3. **Login & Session**: Log in and verify that the session cookie persists across page navigations.
4. **Crop Library**: Visit `/crops`, search for "Rice", and open its cultivation guide.
5. **Chatbot**: Submit a question at `/chatbot` and ensure verified retrieval answers are returned.
6. **Admin Area**: Log in as your newly created administrator and confirm access to `/admin`.

