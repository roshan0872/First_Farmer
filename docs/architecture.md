# First Farmer Agriculture System &mdash; Architecture Guide

## 1. Architectural Philosophy
First Farmer Agriculture System is engineered as **one unified full-stack web application** powered by Python 3.11+ and Flask.

### Core Architecture Decisions:
- **No Split Frontend/Backend**: Everything renders server-side via Jinja2 templates, supplemented by lightweight JSON endpoints under `/api` for interactive asynchronous components (live recommendation scoring, bookmarking, chatbot messages, and Chart.js feeds).
- **Zero Node.js Build Step**: Plain standard CSS using structured design tokens as CSS variables. Client-side interactions utilize lightweight vanilla JavaScript modules.
- **Vendored Dependencies**: Chart.js is completely vendored into `app/static/vendor/` to eliminate external CDN dependencies and enhance privacy/reliability.
- **Portable Database Layer**: Built entirely on SQLAlchemy ORM. Local development runs on zero-configuration SQLite (`instance/first_farmer.db`), while cloud deployment utilizes serverless Neon PostgreSQL via the `psycopg` (v3) binary driver.

---

## 2. Serverless & Vercel Constraints Architecture

When deployed to Vercel, the application functions in an ephemeral, serverless environment:
1. **Read-Only & Ephemeral Filesystem**:
   - The application never writes state, caches, uploads, or session data to the local disk in production.
   - All persistence is centralized in the remote PostgreSQL database (Neon).
2. **Stateless Request Model**:
   - In-memory process dictionaries or global caches are strictly prohibited.
   - User sessions are stored via signed, tamper-proof client cookies (`HttpOnly`, `SameSite=Lax`, and `Secure` in production).
   - Rate limiting and login throttling are backed by the database table `login_attempts`.
3. **Database Connection Pooling in Serverless**:
   - Connection pools are configured with `pool_pre_ping=True` and utilize `NullPool` when connected to Neon to prevent stale connections during serverless cold starts.
4. **Resilient External Integrations**:
   - All third-party network calls (OpenWeatherMap API, optional AI providers) enforce strict 5-second timeouts to prevent hung serverless workers.

---

## 3. Directory & Blueprint Architecture

```
first-farmer-agriculture-system/
├── app.py                      # Root WSGI entry point exposing `app`
├── vercel.json                 # Vercel deployment specification
├── requirements.txt            # Pinned Python package dependencies
├── .env.example                # Template configuration environment variables
├── app/
│   ├── __init__.py             # Application factory (create_app)
│   ├── extensions.py           # db, migrate, csrf, argon2 PasswordHasher
│   ├── config/
│   │   ├── __init__.py         # Dev, Test, Prod configs & DATABASE_URL normalizer
│   │   └── recommendation_rules.py # Scoring weights and thresholds
│   ├── models/                 # Normalized SQLAlchemy models
│   ├── blueprints/             # Modular application controllers
│   ├── services/               # Recommendation, Weather, Chatbot, i18n, Security
│   ├── forms.py                # Flask-WTF and WTForms validation schemas
│   ├── i18n/                   # en.json, ta.json, hi.json locale dictionaries
│   ├── templates/              # Jinja2 templates
│   └── static/                 # CSS tokens, JS modules, SVG illustrations, vendored Chart.js
├── seed/                       # Structured JSON/Python seed content & idempotent seeder
├── tests/                      # Pytest automated test suite
└── docs/                       # Architecture, DB schema, API guide, deployment, and i18n review
```

