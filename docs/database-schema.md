# First Farmer Agriculture System &mdash; Database Schema

## 1. Overview
The schema is designed using normalized relational principles, portable SQL data types, foreign key constraints with explicit cascading delete rules, and strategic indexes on search, filter, and lookup columns.

---

## 2. Entity-Relationship Definitions

### A. User & Security
- `users`:
  - `id` (INTEGER, PK)
  - `full_name` (VARCHAR(120), NOT NULL)
  - `email` (VARCHAR(180), UNIQUE, INDEX)
  - `password_hash` (VARCHAR(255), NOT NULL) &mdash; Argon2id hash
  - `role` (VARCHAR(20), DEFAULT 'student') &mdash; 'student', 'admin'
  - `preferred_language` (VARCHAR(10), DEFAULT 'en') &mdash; 'en', 'ta', 'hi'
  - `created_at`, `updated_at` (DATETIME(timezone=True))
- `login_attempts`:
  - `id` (INTEGER, PK)
  - `key_hash` (VARCHAR(128), UNIQUE, INDEX) &mdash; SHA-256 hash of email:IP
  - `attempts_count` (INTEGER, DEFAULT 1)
  - `last_attempt_at` (DATETIME(timezone=True))
  - `locked_until` (DATETIME(timezone=True), NULLABLE)
- `activity_logs`:
  - `id` (INTEGER, PK)
  - `user_id` (INTEGER, FK -> users.id ON DELETE SET NULL, INDEX)
  - `action` (VARCHAR(80))
  - `entity_type` (VARCHAR(80))
  - `entity_id` (INTEGER, NULLABLE)
  - `created_at` (DATETIME(timezone=True))

### B. Agricultural Entities & Lookups
- `soil_types`: `id`, `name` (UNIQUE, INDEX), `description`
- `seasons`: `id`, `name` (UNIQUE, INDEX), `period`, `description`
- `regions`: `id`, `name` (UNIQUE, INDEX), `state`, `zone`
- Junction Tables:
  - `crop_soils`: `(crop_id, soil_type_id)` Composite PK
  - `crop_seasons`: `(crop_id, season_id)` Composite PK
  - `crop_regions`: `(crop_id, region_id)` Composite PK
- `crops`:
  - `id` (INTEGER, PK)
  - `slug` (VARCHAR(80), UNIQUE, INDEX)
  - `name` (VARCHAR(100), INDEX)
  - `scientific_name` (VARCHAR(120))
  - `category` (VARCHAR(60), INDEX) &mdash; Cereal, Pulse, Vegetable, Fruit, Cash Crop, Millets
  - `description` (TEXT)
  - `water_requirement` (VARCHAR(20)) &mdash; Low, Medium, High
  - `season_summary` (VARCHAR(200))
  - `soil_climate_summary` (TEXT)
  - `image_path` (VARCHAR(255))
  - `min_temp`, `max_temp` (FLOAT)
  - `min_rainfall`, `max_rainfall` (FLOAT)
  - `climate_source_note` (VARCHAR(255))
  - `difficulty_level` (VARCHAR(30)) &mdash; Beginner, Intermediate, Advanced
  - `is_published` (BOOLEAN, DEFAULT TRUE, INDEX)
  - `created_at`, `updated_at` (DATETIME(timezone=True))
- `farm_profiles`:
  - `id` (INTEGER, PK)
  - `user_id` (INTEGER, FK -> users.id ON DELETE CASCADE, INDEX)
  - `region`, `soil_type`, `season`, `water_availability`
  - `temperature`, `rainfall` (FLOAT)
  - `source_information` (VARCHAR(255))
  - `updated_at` (DATETIME(timezone=True))

### C. Guides & Products
- `cultivation_guides`:
  - `id` (INTEGER, PK)
  - `crop_id` (INTEGER, FK -> crops.id ON DELETE CASCADE, UNIQUE, INDEX)
  - `seed_selection`, `land_preparation`, `sowing_method`, `irrigation`, `nutrient_management`, `weed_management`, `growth_stages`, `common_mistakes` (TEXT)
  - `source_reference`, `last_reviewed_at` (VARCHAR(255))
- `pests_diseases`:
  - `id` (INTEGER, PK)
  - `crop_id` (INTEGER, FK -> crops.id ON DELETE CASCADE, INDEX)
  - `name` (VARCHAR(120), INDEX)
  - `type` (VARCHAR(40)) &mdash; pest, disease, other
  - `symptoms`, `contributing_conditions`, `prevention`, `management` (TEXT)
  - `source_reference`, `last_reviewed_at` (VARCHAR(255))
- `harvest_guides`:
  - `id` (INTEGER, PK)
  - `crop_id` (INTEGER, FK -> crops.id ON DELETE CASCADE, UNIQUE, INDEX)
  - `maturity_indicators`, `approximate_harvest_period`, `harvesting_method`, `handling_precautions`, `storage_preparation` (TEXT)
  - `source_reference`, `last_reviewed_at` (VARCHAR(255))
- `post_harvest_guides`:
  - `id` (INTEGER, PK)
  - `crop_id` (INTEGER, FK -> crops.id ON DELETE CASCADE, UNIQUE, INDEX)
  - `cleaning_and_grading`, `storage_method`, `preservation_method`, `processing_method`, `packaging_method`, `food_uses`, `industrial_uses`, `by_products` (TEXT)
  - `source_reference`, `last_reviewed_at` (VARCHAR(255))
- `crop_products`:
  - `id` (INTEGER, PK)
  - `crop_id` (INTEGER, FK -> crops.id ON DELETE CASCADE, INDEX)
  - `product_name` (VARCHAR(120), INDEX)
  - `product_category` (VARCHAR(60)) &mdash; Food Product, Industrial Product, By-Product
  - `raw_material`, `processing_overview`, `common_uses`, `storage_considerations`, `value_addition_notes` (TEXT)

### D. Learning & Engagement
- `crop_bookmarks`: `id`, `user_id`, `crop_id`, `created_at`, UNIQUE(user_id, crop_id)
- `crop_views`: `id`, `user_id`, `crop_id`, `viewed_at`
- `learning_modules`: `id`, `crop_id`, `slug` (UNIQUE, INDEX), `title`, `content_summary`, `sort_order`
- `learning_progress`: `id`, `user_id`, `learning_module_id`, `completion_status`, `progress_percentage`, `last_accessed_at`, UNIQUE(user_id, learning_module_id)
- `quiz_questions`: `id`, `crop_id`, `question_text`, `option_a`, `option_b`, `option_c`, `option_d`, `correct_option`, `explanation`
- `quiz_attempts`: `id`, `user_id`, `crop_id`, `score`, `total_questions`, `completed_at`
- `chat_messages`: `id`, `user_id`, `conversation_id`, `role`, `message_text`, `created_at`
- `translations`: `id`, `entity_type`, `entity_id`, `field_name`, `language_code`, `translated_title`, `translated_content`, UNIQUE(entity_type, entity_id, field_name, language_code)

