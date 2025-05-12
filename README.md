# BuzzBrief 📰

![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![License: MIT](https://img.shields.io/badge/license-MIT-blue)

BuzzBrief is a comprehensive full-stack news aggregation and presentation platform designed to provide users with up-to-date, AI-enhanced news experiences. It features automated scraping from multiple sources, advanced deduplication, AI-powered summarization, and audio playback of articles.

---

## 🌟 Table of Contents

1. [Key Features](#key-features)
2. [Architecture & Tech Stack](#architecture--tech-stack)
3. [Prerequisites](#prerequisites)
4. [Environment Variables](#environment-variables)
5. [Installation & Setup](#installation--setup)

   * [Clone the Repository](#clone-the-repository)
   * [Backend Setup](#backend-setup)
   * [Frontend Setup](#frontend-setup)
   * [ETL Pipeline](#etl-pipeline)
6. [Configuration Files](#configuration-files)
7. [Running Tests](#running-tests)
8. [Project Structure](#project-structure)
9. [API Reference](#api-reference)
10. [Frontend Routes & Behavior](#frontend-routes--behavior)
11. [Deployment](#deployment)
12. [Troubleshooting](#troubleshooting)
13. [Future Roadmap](#future-roadmap)
14. [Contributing](#contributing)
15. [Acknowledgments](#acknowledgments)
16. [License](#license)

---

## 🔑 Key Features

* **Multi-Source Scraping**: Scrapes news from The Times of India, Economic Times, Hindustan Times, and custom RSS feeds.
* **Robust ETL Pipeline**: Uses Scrapy, Pandas, and LeanMinHash for extraction, transformation, deduplication, and loading.
* **FastAPI Backend**: High-performance RESTful API with Pydantic models for validation.
* **AI Summarization**: Utilizes the Hugging Face `sshleifer/distilbart-cnn-12-6` model for chunk-wise summarization of lengthy articles.
* **Audio Generation**: Integrates Azure Cognitive Services for text-to-speech, storing MP3 files in Supabase Storage.
* **Supabase Integration**: Postgres database for metadata, Supabase Storage for media, and Supabase Auth support (future).
* **Modern React Frontend**: Built with Vite, React Router, React DatePicker, and Tailwind CSS for responsive UI and infinite scrolling.
* **Customization & Extensibility**: Easily add new news sources, adjust deduplication thresholds, or swap ML models.

---

## 🏗 Architecture & Tech Stack

| Layer              | Components & Libraries                           |
| ------------------ | ------------------------------------------------ |
| **Extraction**     | Python, Scrapy, dateutil, BeautifulSoup          |
| **Transformation** | Python, Pandas, NLTK, LeanMinHash (`datasketch`) |
| **Loading**        | asyncpg, Supabase Python Client                  |
| **Backend API**    | FastAPI, Pydantic, Uvicorn                       |
| **Summarization**  | Hugging Face Transformers, tokenizers            |
| **Text-to-Speech** | Azure Speech SDK, Supabase Storage               |
| **Frontend**       | React, Vite, React Router, Tailwind CSS, Axios   |
| **CI/CD**          | GitHub Actions, pytest, Flake8                   |

---

## 📋 Prerequisites

* **Node.js** v16 or higher
* **npm** (comes with Node.js)
* **Python** 3.9 or higher
* **Git** 2.20+
* **Supabase** account
* **Azure Cognitive Services** resource for TTS

---

## 🔧 Environment Variables

Create a `.env` file in the root or within `Backend/` with:

```dotenv
# Database & Supabase
DB_URL=postgresql://<user>:<pass>@<host>:5432/<db_name>
SUPABASE_URL=https://<project>.supabase.co
SUPABASE_SERVICE_ROLE_KEY=<service-role-key>

# Azure Text-to-Speech
AZURE_SPEECH_KEY=<azure-key>
AZURE_SPEECH_REGION=<azure-region>

# FastAPI
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=info

# Frontend (Vite)
VITE_API_URL=http://localhost:8000
```

> 💡 **Tip:** Never commit `.env` to version control. Use GitHub Secrets for CI/CD.

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Anubhavnatani04/collegeProject.git
cd collegeProject
```

### 2. Backend Setup

```bash
cd Backend
# Install dependencies
pip install -r ../requirements.txt

# Start the FastAPI server
env $(cat ../.env) uvicorn main:app --reload --host $API_HOST --port $API_PORT
```

* Navigate to `http://localhost:8000/docs` for automatic Swagger UI.

### 3. Frontend Setup

```bash
cd ../frontend
npm install
npm run dev
```

* App available at `http://localhost:5173` by default. Proxy configured to backend.

### 4. ETL Pipeline

ETL jobs are automatically scheduled via [Trigger.dev](https://trigger.dev) to run at regular intervals. To manually trigger or monitor runs, visit the Trigger.dev dashboard configured for this project.

---

## 🔍 Configuration Files

* **`requirements.txt`**: Python dependencies for backend & ETL.
* **`pyproject.toml`**: Poetry metadata (if used).
* **`tsconfig.json`**: TypeScript config (if TS is added).
* **`.prettierrc` / `.eslintrc`**: Frontend formatting & linting rules.

---

## ✅ Running Tests & Linting

1. **Backend Tests**

   ```bash
   cd Backend
   ```

docker-compose run api pytest --cov

````
2. **Frontend Tests** (if configured with Jest):
```bash
cd frontend
npm run test
````

3. **Linting**:

   ```bash
   # Python
   flake8 Backend etl news_scraper
   # JS/TS
   npm run lint --prefix frontend
   ```

---

## 📂 Project Structure

```
collegeProject/
│
├── Backend/                # FastAPI backend
│   ├── main.py             # API route definitions & startup
│   ├── models.py           # Pydantic schemas & DB models
│   ├── summarizer.py       # Chunking & summarization logic
│   ├── audio_service.py    # Azure TTS integration
│   └── utils/              # Helpers for DB, logging, etc.
│
├── etl/                    # ETL orchestrator
│   ├── Extract.py          # Runs Scrapy spiders
│   ├── Transform.py        # Cleans & normalizes text
│   ├── Load.py             # Inserts into DB with dedupe
│   └── Master.py           # Entry point for pipeline
│
├── news_scraper/           # Scrapy project
│   └── news_scraper/       # Auto-generated Scrapy structure
│
├── frontend/               # React + Vite
│   ├── public/             # Static assets & index.html
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Route-specific pages
│   │   ├── hooks/          # Custom React hooks
│   │   └── lib/api.js      # Axios API wrappers
│   └── package.json        # NPM dependencies & scripts
│
├── requirements.txt        # Python deps for backend & ETL
├── pyproject.toml          # (Optional) Poetry config
├── .env.example            # Sample environment variables
└── LICENSE
```

---

## 🗄️ Database Schema

Below is the Supabase/Postgres schema for BuzzBrief, showing the tables and relationships used to store articles, categories, summaries, audio requests, and deduplication indices:

```text
┌────────────────┐            ┌────────────┐
│   articles     │            │ categories │
│  (article_id)  │◀───────────┤   (id)     │
│ headline       │            │ name       │
│ image_url      │            └────────────┘
│ content        │
│ source         │            ┌─────────────────┐      ┌────────────┐
│ url            │            │ article_category│      │ summaries  │
│ published_at   │            │  (id)           │      │  (id)      │
│ description    │◀───────────┤ article_id      │      │ article_id │
│ title_hash     │            │ category_id     │      │ summary    │
│ content_hash   │            └─────────────────┘      │ last_updated│
│ entities       │                                      └────────────┘
│ time_window    │
│ is_kid_friendly│            ┌───────────────┐      ┌──────────────┐
│ created_at     │            │ audio_requests│      │ hash_index   │
└────────────────┘            │  (id)         │      │ fingerprint  │
                              │ article_id    │      │ article_ids  │
                              │ type          │      └──────────────┘
                              │ audio_url     │
                              │ requested_at  │
                              └───────────────┘
```

**Table Descriptions:**

* **articles**: Stores news articles, with text content, metadata, hashing fields for deduplication, and flags like `is_kid_friendly`.
* **categories**: Lookup table for news categories (e.g. politics, tech, sports).
* **article\_category**: Many-to-many pivot between `articles` and `categories`.
* **summaries**: AI-generated summaries for articles, with a timestamp of last update.
* **audio\_requests**: Tracks text-to-speech requests, storing generated MP3 URLs and request timestamps.
* **hash\_index**: Maintains MinHash fingerprints and references to article IDs for deduplication checks.

---

## 📖 API Reference

> **Base URL:** `http://localhost:8000`

| Endpoint                       | Method | Description                                           |
| ------------------------------ | ------ | ----------------------------------------------------- |
| `/health`                      | GET    | Liveness & readiness probe (returns `{status: "OK"}`) |
| `/articles`                    | GET    | Paginated articles list (`?offset=&limit=`)           |
| `/articles/{id}`               | GET    | Detailed article by UUID                              |
| `/articles/{id}/summary`       | GET    | AI-generated summary                                  |
| `/articles/{id}/summary/audio` | GET    | Audio URL for summary MP3                             |
| `/categories/{name}/articles`  | GET    | Articles filtered by category                         |
| `/dates/{YYYY-MM-DD}/articles` | GET    | Articles on a specific date                           |

Use Swagger UI at `/docs` for interactive testing.

---

## 📱 Frontend Routes & Behavior

* **`/` (Home)**: Shows latest & trending articles. Filters for date & category.
* **`/article/:id`**: Full article view, summary generator, and audio player.
* **`/about`**: Project overview & contributor info.

### UI Interactions

* **Infinite Scroll**: Loads next batch of articles when scrolling.
* **Date Picker**: Filter articles by publish date.
* **Generate Summary**: Click to fetch and display a concise summary.
* **Play Audio**: Streams audio from Supabase.

---

## ☁️ Deployment

Deployment of the frontend and backend can be configured on any hosting platform of your choice (e.g., Vercel for frontend, Azure App Service for backend). Ensure environment variables are set in your chosen CI/CD system and that the Trigger.dev service is authorized to invoke the ETL workflows.

---

## 🛠 Troubleshooting

* **API Errors**: Check `.env` values, run `uvicorn` logs.
* **DB Connection**: Verify `DB_URL` and network access to Supabase.
* **TTS Failures**: Confirm Azure key/region and service limits.
* **Frontend 404s**: Ensure proxy in `vite.config.js` matches backend URL.

---

## 🚧 Future Roadmap

* 🛡️ User Authentication & Profiles
* 📌 Bookmarking & Reading Lists
* 🔄 Scheduled ETL via trigger.dev (runs every 3 hours)
* 📊 Analytics Dashboard & Metrics
* ☁️ Localization & Multi-language Support
* 🧪 End-to-End Testing

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/your-feature`)
3. Commit your changes (`git commit -m "feat: add new feature"`)
4. Push to your branch (`git push origin feat/your-feature`)
5. Open a Pull Request

Please follow the code style, update tests, and document changes.

---

## 🙏 Acknowledgments

* [Scrapy](https://scrapy.org/) for robust web crawling.
* [FastAPI](https://fastapi.tiangolo.com/) for backend simplicity.
* [Hugging Face](https://huggingface.co/) for powerful NLP models.
* [Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/) for TTS.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

*Happy coding and may your news always be buzzing!* 🚀
