
# Supabase Database Schema

## Tables and Relationships

---

### `articles`

Stores metadata and content for articles.

| Column         | Type      | Description               |
|----------------|-----------|---------------------------|
| id             | uuid      | Primary Key               |
| headline       | text      | Article headline          |
| image_url      | text      | URL of the image          |
| content        | text      | Full content              |
| source         | text      | Source of the article     |
| url            | text      | Article URL               |
| published_at   | timestamp | Publish timestamp         |
| description    | text      | Article description       |
| title_hash     | int8      | Hash of the title         |
| content_hash   | bytea     | Hash of the content       |
| entities       | _text     | Entities extracted        |
| time_window    | timestamp | Time window for analysis  |
| is_kid_friendly| bool      | Kid-friendly flag         |
| created_at     | timestamp | Record creation time      |

---

### `summaries`

Summarized content of articles.

| Column       | Type      | Description            |
|--------------|-----------|------------------------|
| id           | uuid      | Primary Key            |
| article_id   | uuid      | FK to `articles.id`    |
| summary      | text      | Article summary        |
| last_updated | timestamp | Last update timestamp  |

---

### `audio_requests`

Stores requests for audio versions of articles.

| Column       | Type        | Description            |
|--------------|-------------|------------------------|
| id           | uuid        | Primary Key            |
| article_id   | uuid        | FK to `articles.id`    |
| type         | text        | Request type           |
| audio_url    | text        | URL to generated audio |
| requested_at | timestamptz | Request timestamp      |

---

### `hash_index`

Used to store article hash fingerprints.

| Column     | Type     | Description                   |
|------------|----------|-------------------------------|
| fingerprint| text     | Hash fingerprint              |
| article_ids| _uuid    | Array of article UUIDs        |

---

### `article_category`

Join table between articles and categories.

| Column     | Type  | Description             |
|------------|-------|-------------------------|
| id         | uuid  | Primary Key             |
| article_id | uuid  | FK to `articles.id`     |
| category_id| uuid  | FK to `categories.id`   |

---

### `categories`

Stores predefined article categories.

| Column | Type | Description        |
|--------|------|--------------------|
| id     | uuid | Primary Key        |
| name   | text | Category name      |

---

## Relationships

- `summaries.article_id` → `articles.id`
- `audio_requests.article_id` → `articles.id`
- `hash_index.article_ids` → `articles.id`
- `article_category.article_id` → `articles.id`
- `article_category.category_id` → `categories.id`
