# First Farmer Agriculture System &mdash; API Guide

All REST JSON endpoints are prefixed under `/api` and return standardized JSON payloads with correct HTTP status codes. CSRF protection applies to state-changing endpoints.

---

## 1. Authentication Endpoints

### `GET /api/auth/me`
Retrieves the currently authenticated user session.
- **Response 200**:
  ```json
  {
    "authenticated": true,
    "user": {
      "id": 1,
      "full_name": "Priya Sharma",
      "email": "student@firstfarmer.org",
      "role": "student",
      "preferred_language": "en"
    }
  }
  ```

### `POST /api/auth/register`
Creates a learner user account.
- **Body**: `{"full_name": "...", "email": "...", "password": "...", "preferred_language": "en|ta|hi"}`
- **Response 201**: Returns created user object.
- **Response 409**: Duplicate email conflict.

### `POST /api/auth/login`
Authenticates a user and starts a secure cookie session. Subject to database-backed throttling.
- **Body**: `{"email": "...", "password": "..."}`
- **Response 200**: Session established.
- **Response 401**: Generic error: `"The email or password you entered is incorrect. Please try again."`
- **Response 429**: Throttled: `"Too many failed attempts. Please try again in 5 minutes."`

### `POST /api/auth/logout`
Destroys session and logs out.

### `POST /api/auth/change-password`
Protected. Requires `current_password` verification and enforces minimum 8 characters for `new_password`.

---

## 2. Crop & Recommendation Endpoints

### `GET /api/crops`
List published crops with filtering and pagination.
- **Query Params**: `q`, `category`, `water`, `page`, `per_page`
- **Response 200**:
  ```json
  {
    "total": 10,
    "page": 1,
    "pages": 1,
    "items": [...]
  }
  ```

### `GET /api/crops/<id>`
Fetch full entity details for a single crop.

### `POST /api/recommendations`
Rule-based evaluation algorithm comparing conditions against crop requirements.
- **Body**:
  ```json
  {
    "soil_type": "Loamy",
    "season": "Kharif",
    "water_availability": "High",
    "region": "Tamil Nadu (Cauvery Delta)",
    "temperature": 28.5,
    "rainfall": 1000
  }
  ```
- **Response 200**:
  ```json
  {
    "disclaimer": "Preliminary educational suggestion. Verify with local agricultural guidance and a soil test before making cultivation decisions.",
    "total_results": 4,
    "ranked_crops": [
      {
        "crop": {...},
        "score": 92,
        "match_category": "Strong match",
        "matched_criteria": [...],
        "conflicts": [],
        "explanation": "..."
      }
    ],
    "missing_fields": []
  }
  ```

---

## 3. Crop Detail Guides

- `GET /api/crops/<id>/cultivation`: Returns full cultivation guide with seed selection, irrigation, nutrient, weed, growth stages, and common mistakes.
- `GET /api/crops/<id>/pests-diseases`: Returns documented pests and diseases with IPM protocols.
- `GET /api/crops/<id>/harvest`: Returns maturity indicators, harvest timing, precautions, and storage prep.
- `GET /api/crops/<id>/post-harvest`: Returns handling, cleaning, grading, storage, and processing.
- `GET /api/crops/<id>/products`: Returns value-added products catalog for the crop.

---

## 4. Bookmarks & Progress Endpoints

- `GET /api/bookmarks`: Protected. Returns list of bookmarked crops.
- `POST /api/bookmarks/<crop_id>`: Protected. Adds crop to user bookmarks.
- `DELETE /api/bookmarks/<crop_id>`: Protected. Removes crop from bookmarks.
- `GET /api/progress`: Protected. Returns user's module progress percentages.
- `POST /api/progress/<module_id>`: Protected. Updates completion status (`"completed"` or `"in_progress"`).

---

## 5. Weather Endpoint

### `GET /api/weather?location=<city>`
Returns live OpenWeather observations or explicit educational fallback.
- **Response 200**:
  ```json
  {
    "is_live": false,
    "provider": "Sample Educational Provider (No API key configured)",
    "notice": "Sample data — not live weather.",
    "location": "Coimbatore",
    "temperature_c": 28.5,
    "humidity_percent": 68,
    "wind_speed_kmh": 12.0,
    "condition": "Partly Cloudy",
    "advisories": [...]
  }
  ```

---

## 6. Chatbot Endpoints

### `POST /api/chat`
Processes questions using database retrieval. If AI keys are set, grounds response.
- **Body**: `{"message": "How to manage fruit borer in tomato?", "conversation_id": "..."}`
- **Response 200**:
  ```json
  {
    "answer": "...",
    "link_url": "/pests-diseases?crop=4",
    "link_text": "View Tomato Pest Guide",
    "mode": "retrieval",
    "is_ai": false,
    "disclaimer": "Educational assistance only. For field diagnostic emergencies, consult your local agricultural extension officer."
  }
  ```

### `DELETE /api/chat/history`
Protected. Clears all stored conversation records for current user.

---

## 7. Administrative CRUD Endpoints
Protected by server-side `@admin_required` checks:
- `POST /api/crops`: Create new crop
- `PUT /api/crops/<id>`: Update crop
- `DELETE /api/crops/<id>`: Delete crop and cascading guides

