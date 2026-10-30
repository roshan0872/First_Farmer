# First Farmer Agriculture System

> **"Learn Agriculture. Grow Knowledge. Discover Value."**

First Farmer Agriculture System is a complete, educational, and assistive agricultural learning platform built with Flask, Jinja2, vanilla CSS/JavaScript, SQLite for local development, and Neon Serverless PostgreSQL for Vercel deployment.

---

## 1. System Requirements & Technology Stack

- **Python Runtime:** Python 3.11, 3.12, 3.13, or 3.14 (Vercel uses Python 3.11+)
- **Application Engine:** Flask 3.1+ with Application Factory and Blueprints
- **ORM & Data Layer:** SQLAlchemy 2.0+ with Flask-SQLAlchemy and Flask-Migrate (Alembic)
- **Database Drivers:**
  - Local / Tests: SQLite (`instance/first_farmer.db` or `:memory:`)
  - Production (Vercel): Neon Serverless PostgreSQL via `psycopg[binary]` (v3)
- **Security & Forms:** Flask-WTF, WTForms, `argon2-cffi` (Argon2id password hashing)
- **External Calls:** `requests` with strict 5-second timeouts
- **Front-end Design:** Custom Forest Green Design Tokens (`#1F5135`), responsive vanilla JavaScript, vendored Chart.js (no CDN dependency), inline Lucide SVGs
- **Multilingual Support:** English (`en`), Tamil (`ta`), and Hindi (`hi`)

---

## 2. Local Setup & Quickstart

Clone or extract the repository, open your terminal in the project root, and execute the following:

### Windows (PowerShell)

```powershell
# 1. Create a virtual environment
python -m venv .venv

# 2. Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# 3. Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Copy the environment template
Copy-Item .env.example .env

# 5. Seed the local SQLite database with 10 crops and guides
python seed/seed.py

# 6. Start the application with one command
python app.py
```

### macOS / Linux

```bash
# 1. Create a virtual environment
python3 -m venv .venv

# 2. Activate the virtual environment
source .venv/bin/activate

# 3. Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Copy the environment template
cp .env.example .env

# 5. Seed the local SQLite database
python seed/seed.py

# 6. Start the application with one command
python app.py
```

Open your browser to: **`http://127.0.0.1:5000`**

---

## 3. Development Credentials & Accounts

The development database seeder creates two ready-to-use sample accounts:

| Role | Email | Password |
|---|---|---|
| **Student / Learner** | `student@firstfarmer.org` | `StudentPass123!` |
| **Administrator** | `admin@firstfarmer.org` | `AdminPass123!` |

> **IMPORTANT:** These demo credentials are strictly for development. The seed script **automatically refuses to create demo accounts when `APP_ENV=production`**.

To create a secure administrator account interactively in any environment without hardcoding passwords:
```bash
flask create-admin
```

---

## 4. Running Automated Tests

Run the full pytest suite with isolated in-memory databases:

```bash
pytest -v
```

All 18 tests cover registration, duplicate email rejection, login throttling, administrator role authorization (HTTP 403 enforcement), crop filtering, recommendation matching, bookmarking, chatbot retrieval, weather mock timeouts, and language switching.

---

## 5. Configuring Optional External Services

Edit your `.env` file to configure external integrations:

### Live Weather Guidance (OpenWeatherMap)
1. Sign up for a free key at [OpenWeatherMap](https://openweathermap.org/api).
2. Set `WEATHER_API_KEY=your_key_here`.
3. If left blank, the application displays a clearly labeled simulation banner: **"Sample data — not live weather."**

### Grounded Chatbot AI Provider (Optional)
By default, the chatbot runs as a **verified retrieval-based assistant** querying the local database without external dependencies.
If you wish to enable server-grounded AI responses:
```env
AI_PROVIDER=gemini
AI_API_KEY=your_gemini_api_key
```

---

## 6. Deployment Guide: GitHub &rarr; Neon Postgres &rarr; Vercel

The application is architected from day one for Vercel's serverless runtime and Neon's serverless Postgres.

### Step 1: Create a Neon Database
1. Go to [Neon.tech](https://neon.tech) and create a free project named `first-farmer`.
2. In the dashboard, copy the **Pooled connection string**. It looks like:
   ```
   postgresql://user:password@ep-xyz-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

### Step 2: Seed Neon from Your Machine
Because Vercel serverless functions have a read-only filesystem and ephemeral workers, migrations and database seeding must run once from your developer machine:

**Windows (PowerShell):**
```powershell
$env:DATABASE_URL="postgresql+psycopg://user:password@ep-xyz-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
python seed/seed.py --content-only
flask create-admin
```

**macOS / Linux:**
```bash
export DATABASE_URL="postgresql+psycopg://user:password@ep-xyz-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
python seed/seed.py --content-only
flask create-admin
```

### Step 3: Push to GitHub
Make sure `.env` and SQLite `.db` files are ignored:
```bash
git add .
git commit -m "Production release for Vercel"
git push origin main
```

### Step 4: Import to Vercel
1. In the [Vercel Dashboard](https://vercel.com/dashboard), click **Add New &rarr; Project** and select your GitHub repository.
2. Configure **Environment Variables**:
   - `APP_ENV`: `production`
   - `SECRET_KEY`: *(Set a strong 32+ character random string)*
   - `DATABASE_URL`: *(Your pooled Neon PostgreSQL URL)*
   - `WEATHER_API_KEY`: *(Optional OpenWeatherMap API key)*
   - `AI_PROVIDER`: *(Optional)*
   - `AI_API_KEY`: *(Optional)*
3. Click **Deploy**.

---

## 7. Troubleshooting & Common Pitfalls

| Issue | Root Cause | Solution |
|---|---|---|
| **App refuses to start in Production** | `SECRET_KEY` is missing or set to `change-me` | Provide a cryptographically random secret key in `SECRET_KEY`. |
| **Neon SSL Connection Error** | Missing `sslmode=require` in URL | `normalize_database_url` appends `sslmode=require` automatically; ensure `postgresql+psycopg://` driver scheme is used. |
| **Serverless Cold Starts** | Stale connection pool | The app automatically uses `NullPool` and `pool_pre_ping=True` when running against PostgreSQL. |
| **Tamil or Hindi Text Not Rendering** | Missing system font | `base.html` embeds Google Fonts fallbacks for `Noto Sans Tamil` and `Noto Sans Devanagari`. |
| **Database-backed Login Throttling** | 5 consecutive bad passwords | Locks the IP/email combination for 5 minutes. The counter resets automatically after the window expires. |

---

## 8. License & Agronomic Disclaimer

This platform is developed for educational and assistive purposes under the MIT License. Agricultural recommendations represent baseline scientific guidance and must never replace localized field soil tests and advice from local certified agricultural extension officers.
