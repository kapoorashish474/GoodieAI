# System Design: Real-Time Hacker News Analytics Dashboard

## ✨ Overview

A scalable, event-driven, full-stack web application that fetches top Hacker News stories, processes them for AI-related trends and brand mentions, and displays analytics in a dashboard interface. The architecture is built with modular, extensible services and optimized for future enhancements like real-time updates or multi-source ingestion.

---

---

## 🔍 Goals

* Extract top 50 HN stories and store relevant metadata
* Detect AI-related topics and brands from story titles
* Visualize processed analytics in a frontend dashboard
* Provide searchable and filterable story explorer

---

## 💡 Architectural Overview

### Tech Stack

| Component       | Technology                       |
| --------------- | -------------------------------- |
| Backend         | FastAPI (Python)                 |
| Async Tasks     | Celery + brew install node                   |
| Messaging Queue | Redis Pub/Sub                    |
| Database        | PostgreSQL                       |
| Frontend        | Next.js (App Router, TypeScript) |

### Services

1. **Service A: Main API Service**

   * Exposes REST API (OpenAPI documented)
   * Manages DB schema and story persistence
   * Publishes events when new stories are fetched
   * Aggregates insights (from Service B)
2. **Service B: Background Processing Service**

   * Subscribes to story events
   * Detects AI-related brands via NLP
   * Aggregates keyword frequencies & domains
   * Persists analysis to PostgreSQL

---

## 📑 Data Flow

1. Service A fetches `/v0/topstories.json` + `/v0/item/{id}.json`
2. Extracts fields: `title`, `url`, `score`, `descendants`, `by`, `time`
3. Saves raw story data to PostgreSQL
4. Publishes event (`new_story:<story_id>`) via Redis
5. Service B listens to Redis, processes story titles:

   * Detect brands: ChatGPT, Claude, Gemini, etc.
   * Extract keywords/domains
   * Update aggregated tables
6. Frontend fetches via Service A:

   * Raw story data
   * Brand frequency
   * Domain trends

---

## 📊 Database Schema (PostgreSQL)

### Table: `stories`

| Field       | Type      | Notes               |
| ----------- | --------- | ------------------- |
| id          | INTEGER   | HN story ID (PK)    |
| title       | TEXT      |                     |
| url         | TEXT      |                     |
| time        | TIMESTAMP |                     |
| score       | INTEGER   |                     |
| descendants | INTEGER   | # of comments       |
| author      | TEXT      |                     |
| fetched\_at | TIMESTAMP | For refresh control |

### Table: `analytics`

| Field      | Type      | Notes          |
| ---------- | --------- | -------------- |
| keyword    | TEXT      | e.g. "ChatGPT" |
| count      | INTEGER   | Frequency      |
| last\_seen | TIMESTAMP |                |

### Table: `domains`

| Field  | Type    | Notes           |
| ------ | ------- | --------------- |
| domain | TEXT    | e.g. openai.com |
| count  | INTEGER | Frequency       |

---

## 🚀 Frontend (Next.js + TypeScript)

### Pages:

1. `/dashboard`

   * Keyword frequency chart
   * Top domains bar chart
2. `/explorer`

   * Table view with filters: date range, keyword
3. `/story/[id]`

   * Detailed view (optional)

### UI Libraries:

* Tailwind CSS
* Chart.js or Recharts
* TanStack Table for explorer

### Features:

* Debounced search
* Responsive layout
* Suspense/Error boundaries (optional)

---

## ⚖️ Key Design Decisions

* **Event-driven processing:** clean decoupling of ingestion and analysis
* **Redis Pub/Sub:** lightweight, quick-to-setup messaging
* **FastAPI:** async-friendly, built-in OpenAPI
* **Next.js App Router:** better async rendering & route separation

---

## 📅 Future Scalability

* Add Kafka for robust pub/sub
* Support more sources (e.g. Reddit, Twitter APIs)
* Migrate to GraphQL for complex queries
* Add WebSocket layer for real-time updates

---

## ✔️ Submission Checklist

* [x] Full source code (backend + frontend)
* [x] README with:

  * Setup steps
  * Sequence diagrams
  * Key decisions
  * Scalability plan
* [ ] Optional Enhancements (if time allows)

---

## 🎯 Optional Enhancements (Time Permitting)

* WebSocket live updates
* Saved stories
* Redis caching
* CI/CD with GitHub Actions
* Score vs. comments scatter chart
* Basic unit tests

---

## 💬 Presentation Format (1 Hour)

1. **Architecture Walkthrough** (15 min)

   * Sequence diagram
   * Pub/Sub model
2. **Live Demo** (15 min)

   * Dashboard and Explorer
3. **Code Walkthrough** (15 min)

   * Data ingestion, processing, and API
4. **Q\&A** (15 min)

   * Design decisions, tradeoffs, performance

---

Here’s a summary of the errors you encountered and how to solve them:

---

### 1. **Python Not Found**
- **Error:** `zsh: command not found: python`
- **Solution:** Use `python3` instead of `python` on macOS.

---

### 2. **Pip Externally Managed Environment**
- **Error:**  
  ```
  error: externally-managed-environment
  ```
- **Solution:**  
  - Use a virtual environment (`python3 -m venv venv` and `source venv/bin/activate`).

---

### 3. **Dependency Build Failures (spacy, blis, psycopg2-binary, pydantic-core)**
- **Error:**  
  - Compilation errors for `blis` and `spacy`
  - Build errors for `psycopg2-binary` and `pydantic-core`
- **Root Cause:**  
  - You are using Python 3.13, which is too new for many libraries.
- **Solution:**  
  - **Switch to Python 3.11** (or 3.10).  
    - Install with:  
      ```sh
      brew install python@3.11
      ```
    - Create a new virtual environment:  
      ```sh
      python3.11 -m venv venv
      source venv/bin/activate
      ```
    - Install dependencies:  
      ```sh
      pip install -r requirements.txt
      ```

---

### 4. **Leftover Virtual Environments**
- **Action:**  
  - You deleted the `venv` directory.  
  - If there are others, repeat:  
    ```sh
    rm -rf <venv-folder-name>
    ```

---

## **Next Steps (Recommended Fixes)**

1. **Install Python 3.11:**
   ```sh
   brew install python@3.11
   ```

2. **Create and activate a new virtual environment:**
   ```sh
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run your server:**
   ```sh
   python main.py api --reload
   ```

---

## **Why These Steps Work**

- Python 3.13 is not yet supported by many libraries (especially those with C extensions).
- Python 3.11 is stable and supported by all your dependencies.

---

If you want, I can walk you through each step interactively. Would you like to proceed with installing Python 3.11 and setting up the environment?
