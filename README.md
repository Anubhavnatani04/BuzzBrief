&#x20;&#x20;

# BuzzBrief 📰

**BuzzBrief** is a full-stack, AI-augmented news aggregation and presentation platform. It automatically scrapes articles from top news sources, deduplicates and summarizes content using state-of-the-art NLP models, and presents users with both reading and listening experiences via an intuitive, modern web interface. The goal is to make staying informed faster, smarter, and more engaging for users across all devices.

---

## 🌟 Table of Contents

1. [Key Features](#key-features)
2. [Getting Started](#getting-started)

   * [Prerequisites](#prerequisites)
   * [Environment Setup](#environment-setup)
   * [Installation](#installation)
3. [Project Architecture & Tech Stack](#project-architecture--tech-stack)
4. [Configuration & Secrets](#configuration--secrets)
5. [Usage & Examples](#usage--examples)

   * [API Usage](#api-usage)
   * [Frontend Interaction](#frontend-interaction)
   * [Custom Scraper Example](#custom-scraper-example)
6. [Testing & CI/CD](#testing--cicd)
7. [Project Structure](#project-structure)
8. [Supabase Schema Design](#supabase-schema-design)
9. [Troubleshooting & Tips](#troubleshooting--tips)
10. [Future Roadmap](#future-roadmap)
11. [Contributing](#contributing)
12. [Acknowledgments](#acknowledgments)
13. [License](#license)

---

## 🔑 Key Features

BuzzBrief packs an array of powerful, user-centric features designed to transform how you consume news:

* **Automated Multi-Source Scraping**

  * Collects articles from major outlets like The Times of India, Economic Times, Hindustan Times, and any custom RSS feeds you define.
  * Supports both RSS and HTML parsing—ensuring maximum coverage even when sources lack clean feeds.
  * Configurable scraping intervals and retry logic for robust, error-resilient data collection.

* **Robust ETL Pipeline**

  * **Extract**: Leverages Scrapy with custom spiders for targeted field extraction.
  * **Transform**: Cleans, normalizes, and enriches data using Pandas and NLTK (e.g., date parsing, language detection).
  * **Deduplicate**: Applies LeanMinHash from `datasketch` to identify and discard near-duplicate articles across sources.

* **High-Performance Backend**

  * Built on FastAPI for lightning-fast response times with async I/O and WebSocket support.
  * Full request/response validation using Pydantic models to catch errors early.
  * Auto-generated OpenAPI docs and interactive Swagger UI for easy API exploration.

* **AI-Powered Summarization**

  * Splits long-form articles into digestible chunks and summarizes using Hugging Face’s `distilbart-cnn-12-6`.
  * Customizable summary length and style (e.g., bullet points, narrative).
  * Plug-and-play support for alternative models (e.g., Pegasus, T5) via simple configuration changes.

* **Text-to-Speech Playback**

  * Integrates Azure Cognitive Services to generate natural-sounding audio from summaries.
  * Stores MP3 files in Supabase Storage with CDN-backed delivery for fast, scalable streaming.
  * Supports multiple voice profiles, adjustable speaking rate, and SSML tags for pronunciation control.

* **Real-Time Audio & Text Sync**

  * Synchronizes audio playback with highlighted text segments in real time.
  * Offers continuous scroll or page-by-page reading modes to suit different consumption styles.
  * Visual progress indicators and keyboard shortcuts for accessibility.

* **Responsive React Frontend**

  * Developed with Vite for instant hot-module replacement and minimal build times.
  * Uses React Router for nested routing, Tailwind CSS for utility-first styling, and React DatePicker for advanced filter controls.
  * Infinite scroll and pagination options for seamless navigation through large article volumes.

* **Extensible & Configurable**

  * **Modular architecture**: Add new scrapers, transformers, or summarizers through a plugin-like system.
  * **Environment-driven settings**: Tweak dedupe thresholds, summary lengths, and scraping schedules without code changes.
  * **Feature flags**: Roll out new capabilities (e.g., video summaries) gradually or to specific user cohorts.

* **Dark Mode & Accessibility**

  * Automatic theme switching based on OS preferences, plus manual toggle.
  * ARIA attributes and keyboard navigation support for screen readers.
  * High contrast modes and scalable fonts to meet WCAG 2.1 AA standards.

---

## 🏁 Getting Started

### Prerequisites

Ensure the following tools are installed on your development machine before setup:

* **Node.js** (v16+) for frontend tooling.
* **npm** (v8+) for managing Node packages.
* **Python** (v3.9+) for backend and ETL logic.
* **Git** (v2.20+) for source control.
* **Supabase** account for hosting the database and file storage.
* **Azure Cognitive Services** resource for generating text-to-speech audio.

### Environment Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Anubhavnatani04/collegeProject.git
   cd collegeProject
   ```

2. **Create your environment file** by copying the template:

   ```bash
   cp .env.example .env
   ```

3. \*\*Edit \*\***`.env`** with required configuration:

   ```dotenv
   # Supabase
   DB_URL=postgresql://<USER>:<PASS>@<HOST>:5432/<DB_NAME>
   SUPABASE_URL=https://<PROJECT_REF>.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=<SERVICE_ROLE_KEY>

   # Azure
   AZURE_SPEECH_KEY=<AZURE_KEY>
   AZURE_SPEECH_REGION=<AZURE_REGION>

   # Backend API
   API_HOST=0.0.0.0
   API_PORT=8000
   LOG_LEVEL=info

   # Frontend
   VITE_API_URL=http://localhost:8000
   ```

> **Pro Tip**: Store secrets in GitHub Actions for deployments instead of committing them.

### Installation

#### Backend

1. Navigate to the backend and install dependencies:

   ```bash
   cd Backend
   pip install -r ../requirements.txt
   ```
2. If database migrations are needed:

   ```bash
   alembic upgrade head
   ```
3. Start the development server:

   ```bash
   uvicorn main:app --reload --host $API_HOST --port $API_PORT
   ```

#### Frontend

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   npm install
   ```
2. Start the frontend server:

   ```bash
   npm run dev
   ```
3. View the application in your browser at `http://localhost:5173`.

#### ETL Pipeline

* Job scheduling is automated using [Trigger.dev](https://trigger.dev) and runs every 3 hours.
* For immediate updates, run manually:

  ```bash
  python etl/Master.py
  ```

---

## 🏗 Project Architecture & Tech Stack

| Layer           | Technologies Used                              |
| --------------- | ---------------------------------------------- |
| Data Extraction | Python, Scrapy, BeautifulSoup, dateutil        |
| Transformation  | Pandas, NLTK, LeanMinHash (`datasketch`)       |
| Data Loading    | asyncpg, Supabase Python SDK                   |
| Backend API     | FastAPI, Pydantic, Uvicorn                     |
| Summarization   | Hugging Face Transformers, Tokenizers          |
| Text-to-Speech  | Azure Speech SDK, Supabase Storage             |
| Frontend        | React, Vite, React Router, Tailwind CSS, Axios |
| CI/CD & Testing | GitHub Actions, Pytest, Flake8, Jest           |

---

## 🔧 Configuration & Secrets

| Environment Variable        | Description                                          |
| --------------------------- | ---------------------------------------------------- |
| `DB_URL`                    | PostgreSQL database connection string                |
| `SUPABASE_URL`              | Supabase endpoint URL                                |
| `SUPABASE_SERVICE_ROLE_KEY` | Service-level secret key for Supabase access         |
| `AZURE_SPEECH_KEY`          | Subscription key for Azure Speech Services           |
| `AZURE_SPEECH_REGION`       | Azure Speech Services regional setting               |
| `API_HOST`, `API_PORT`      | Backend API server host and port configuration       |
| `VITE_API_URL`              | URL used by frontend to communicate with backend API |

---

## 🚀 Usage & Examples

### API Usage

* **Fetch Articles**:

```bash
curl "$VITE_API_URL/articles?offset=0&limit=10"
```

* **Get Summary for an Article**:

```bash
curl "$VITE_API_URL/articles/{id}/summary"
```

**Example Output**:

```json
[
  {
    "id": "uuid-example",
    "headline": "Global Market Trends Update",
    "source": "Hindustan Times",
    "published_at": "2025-05-10T14:30:00Z",
    "summary_available": true
  }
]
```

### Frontend Interaction

* **Homepage**: Displays trending and categorized headlines.
* **Filters**: Choose specific dates or categories to view news.
* **Scroll**: New articles automatically load as you scroll.
* **Summarization**: Click to reveal AI-generated summaries.
* **Listen Mode**: Convert summaries into high-quality speech.

### Custom Scraper Example

To add a new scraper:

1. Write a new Scrapy spider in `news_scraper/`.
2. Add logic for parsing RSS/HTML feeds.
3. Integrate with ETL via `etl/Extract.py`.
4. Configure deduplication rules in `Transform.py`.

```python
class CustomSpider(scrapy.Spider):
    name = "custom"
    start_urls = ["https://example.com/rss"]

    def parse(self, response):
        for entry in response.xpath('//item'):
            yield {
                'headline': entry.xpath('title/text()').get(),
                'url': entry.xpath('link/text()').get(),
                'published_at': entry.xpath('pubDate/text()').get(),
                'content': entry.xpath('description/text()').get(),
            }
```

---

## ✅ Testing & CI/CD

* **Run Backend Tests**:

  ```bash
  pytest --cov
  ```
* **Linting**:

  * Python: `flake8 Backend etl news_scraper`
  * JavaScript/TypeScript: `npm run lint --prefix frontend`
* **Frontend Testing**:

  ```bash
  npm test
  ```
* **CI Pipeline**:

  * Triggered on PRs and pushes to main.
  * Includes test runs, linting, and code quality checks.

---

## 📂 Project Structure

The project follows a modular structure, making it easy to locate components and extend functionality:

```
collegeProject/
├── Backend/               # FastAPI application with endpoints, models, and services
│   ├── main.py            # Entry point for server startup
│   ├── models.py          # Pydantic models and database schemas
│   ├── summarizer.py      # Logic for NLP summarization using Hugging Face
│   ├── audio_service.py   # Azure TTS integration and media handling
│   └── utils/             # Helper functions and shared utilities
├── etl/                   # Complete ETL pipeline scripts
│   ├── Extract.py         # Defines extraction logic from various sources
│   ├── Transform.py       # Cleans, normalizes, and deduplicates data
│   ├── Load.py            # Persists data into Supabase/Postgres
│   └── Master.py          # Orchestrates the full ETL workflow
├── news_scraper/          # Scrapy-based spiders for custom source scraping
│   └── spiders/           # Individual spider definitions per source
├── frontend/              # React/Vite client application
│   ├── src/               # JSX components, pages, and hooks
│   ├── public/            # Static assets and index.html
│   └── package.json       # Frontend dependencies and scripts
├── .env.example           # Template for environment variables
├── requirements.txt       # Python dependencies for backend & ETL
├── README.md              # Project documentation (this file)
└── LICENSE                # MIT License details
```

Each directory is organized to separate concerns:

* **Backend**: Contains all server-side logic, from API endpoints to model definitions.
* **ETL**: Houses extraction, transformation, and loading scripts, enabling scheduled or on-demand data processing.
* **news\_scraper**: Encapsulates all custom web scraping spiders, making it simple to add or update sources.
* **frontend**: Holds the user interface code, split into components, pages, and styles for maintainability.

---

## 🗄️ Supabase Schema Design

Below is the comprehensive Supabase (PostgreSQL) schema design for BuzzBrief. It shows how data is structured, indexed, and related for efficient querying, deduplication, and media delivery.

![Supabase Schema](5533376f-26e9-4633-b824-f616cbb57b4e.png)

**Detailed Table Descriptions & Relationships:**

| Table                 | Primary Key          | Fields                                                                                                                                                                                                                              | Indexes                                                                            | Usage                                                          |
| --------------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **articles**          | `id` (UUID)          | `headline`, `content`, `description`, `image_url`, `source`, `url`, `published_at`, `title_hash` (int8), `content_hash` (bytea), `entities` (\_text), `time_window` (timestamp), `is_kid_friendly` (bool), `created_at` (timestamp) | B-tree on `published_at`; GIN on `entities`; hash on `title_hash` & `content_hash` | Central store for all news articles, queried by API & ETL jobs |
| **categories**        | `id` (UUID)          | `name` (text)                                                                                                                                                                                                                       | Unique on `name`                                                                   | Defines taxonomy for articles                                  |
| **article\_category** | `id` (UUID)          | `article_id` → `articles.id`, `category_id` → `categories.id`                                                                                                                                                                       | Composite unique on (`article_id`,`category_id`)                                   | Many-to-many mapping between articles and categories           |
| **summaries**         | `id` (UUID)          | `article_id` → `articles.id`, `summary` (text), `last_updated` (timestamp)                                                                                                                                                          | B-tree on `last_updated`                                                           | Stores generated summaries for quick retrieval                 |
| **audio\_requests**   | `id` (UUID)          | `article_id` → `articles.id`, `type` (text), `audio_url` (text), `requested_at` (timestamptz)                                                                                                                                       | B-tree on `requested_at`                                                           | Tracks TTS conversions and usage analytics                     |
| **hash\_index**       | `fingerprint` (text) | `article_ids` (UUID\[])                                                                                                                                                                                                             | N/A                                                                                | Groups similar articles for deduplication phases               |

**Design Considerations & Best Practices:**
& Best Practices:\*\*

1. **UUID Keys**: Use globally unique identifiers to avoid collision across distributed systems and simplify merges.
2. **Indexing Strategy**: Careful application of GIN, B-tree, and hash indexes balances read performance against write overhead in ETL jobs.
3. **Foreign Key Cascades**: `ON DELETE CASCADE` on summaries and audio\_requests ensures clean removal of dependent records when an article is deleted.
4. **Partitioning by Time Window**: Future enhancements could partition `articles` by `time_window` (e.g., monthly) to improve query performance on large datasets.
5. **Entity Extraction**: Storing `entities` as a JSONB or `_text` array allows faceted search (e.g., show articles mentioning “AI”).
6. **Audit Timestamps**: `created_at` and `last_updated` facilitate debugging, monitoring, and cache invalidation workflows.

These design elements collectively ensure BuzzBrief’s backend remains scalable, maintainable, and performant even as data volume grows.

---

## 🛠 Troubleshooting & Tips

This section covers common issues and their resolutions:

**1. API Server Errors**

* **Symptoms**: `500 Internal Server Error` on API requests.
* **Troubleshoot**: Check `uvicorn` logs with `--reload` flag. Verify Pydantic validation errors in console.

**2. Database Connection Failures**

* **Symptoms**: `could not connect to server` errors.
* **Troubleshoot**: Confirm `DB_URL` format, network access rules, and SSL requirements in Supabase.

**3. Missing or Invalid TTS Output**

* **Symptoms**: Audio playback fails or returns empty file.
* **Troubleshoot**: Ensure `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION` match your Azure resource. Check Azure quotas.

**4. CORS & Frontend Loading Issues**

* **Symptoms**: Browser console shows CORS policy violation.
* **Troubleshoot**: Update FastAPI CORS middleware to include your frontend origin. Adjust `vite.config.js` proxy settings.

**5. ETL Pipeline Stalls or Fails**

* **Symptoms**: ETL job stops mid-run, no new data loaded.
* **Troubleshoot**: Inspect Trigger.dev dashboard logs. Run `python etl/Master.py` locally with debug prints.

---

## 🚧 Future Roadmap

We’re continually enhancing BuzzBrief. Planned milestones include:

* **Q3 2025: User Authentication & Profiles**

  * JWT-based login, registration, and user preference storage.
* **Q4 2025: Bookmarks & Reading Lists**

  * Enable users to save articles, tag topics, and share lists.
* **Q1 2026: Analytics Dashboard**

  * Admin panel with usage metrics, source performance, and user engagement charts.
* **Q2 2026: Internationalization**

  * Add support for non-English news sources and summaries.
* **Q3 2026: Mobile PWA Release**

  * Progressive Web App with offline support and push notifications.

Stay tuned and feel free to suggest enhancements via Issues or Discussions.

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository** on GitHub.
2. **Create a branch**: `git checkout -b feat/your-feature`
3. **Implement** your feature or bug fix.
4. **Write tests** and update documentation where applicable.
5. **Commit changes** using conventional commits: e.g., `feat(scraper): add new RSS parser`.
6. **Push** to your fork: `git push origin feat/your-feature`
7. **Open a Pull Request** against the main branch.

**Contribution Guidelines**:

* Adhere to PEP8 for Python and ESLint rules for JavaScript.
* Ensure all tests pass locally and on CI.
* Provide clear PR descriptions and link relevant issues.

---

## 🙏 Acknowledgments

Special thanks to the open-source projects and communities that make BuzzBrief possible:

* **Scrapy** for powering our web crawlers.
* **FastAPI** for building performant APIs.
* **Hugging Face** for state-of-the-art NLP models.
* **Azure Cognitive Services** for seamless TTS.
* **Trigger.dev** for orchestrating ETL workflows.
* **Tailwind CSS** for utility-first styling.

---

## 📄 License

BuzzBrief is open-sourced under the MIT License. See [LICENSE](LICENSE) for details.

---

*Happy coding, and may your news always be buzzing with insights!* 🚀
