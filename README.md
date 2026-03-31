# Job Market Analytics API

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=flat&logo=render&logoColor=white)](https://render.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An automated, end-to-end data pipeline and RESTful API built to extract, clean, and analyze tech job market trends in real-time. 

Live Deployment: **[Access the API and test endpoints here (Swagger UI)](https://job-market-api-betr.onrender.com/docs)**

---

## Application Overview

This application is a fully automated data engineering pipeline designed to provide actionable intelligence on the current tech job market. 

The architecture follows a strictly defined Data Flow:
1. **Extraction:** An autonomous worker fetches raw job listings from external sources.
2. **Transformation:** Data passes through a cleaning phase (whitelist filtering, seniority classification, and tech stack mapping) to ensure high data quality.
3. **Loading:** Structured data is persisted into a PostgreSQL relational database.
4. **Serving:** A high-performance FastAPI backend exposes the aggregated data through specialized endpoints.

### Key Business Features
* **Job Explorer:** Advanced endpoints to filter opportunities by Technology, Seniority, Location and Company.
* **Market Intelligence:** Aggregated analytics delivering statistical insights (e.g., remote vs. on-site ratios, top trending technologies).
* **Automated ETL Pipeline:** A background script autonomously handles the entire data lifecycle.

### Technical Highlights
* **Containerized Architecture:** Fully dockerized environments ensuring parity across machines.
* **Condition-Based Orchestration:** Advanced Docker Compose setup ensuring services only boot when their dependencies are fully healthy.
* **Hybrid Deployment:** Local environment runs on Docker, while the production environment runs natively on Render with managed PostgreSQL.
* **Automated Testing:** Robust test suite built with pytest for endpoint validation and state isolation.

---

## Local Architecture & Orchestration (Docker)

To ensure a flawless developer experience, the local infrastructure is orchestrated using `docker-compose` with strict **condition-based startup sequences**. This guarantees that no service is exposed or executed before its dependencies are fully resolved.

1. **`db` (PostgreSQL 15):** Bootstraps the relational database. It utilizes a custom Docker `healthcheck` running `pg_isready` to constantly ping the database until it is actively accepting TCP/IP connections, preventing premature downstream execution.
2. **`etl_job` (Ephemeral Worker):** Configured with the `depends_on: service_healthy` condition. It waits for the database to be 100% ready, executes the web-scraping and ETL scripts, populates the database, and exits gracefully (`Exit 0`).
3. **`api` (FastAPI):** Configured with the `depends_on: service_completed_successfully` condition. It remains dormant until the `etl_job` container has finished its execution and terminated. This guarantees the API is never exposed to the user with an empty database.

---

## Getting Started (Zero-Config Local Setup)

The entire infrastructure is Plug-and-Play. No local installation of Python or PostgreSQL is required; Docker handles all environment variables and dependencies.

### 1. Clone the repository
```bash
git clone https://github.com/abreu-joao/job-market-analytics-api.git
cd job-market-analytics-api
```

### 2. Run the fully orchestrated environment
```bash
docker-compose up --build
```

### 3. Access the API
Once the terminal displays `API is ON! Access: http://localhost:8000`, open your browser:
**[http://localhost:8000/docs](http://localhost:8000/docs)**

To shut down and clean up the environment:
```bash
docker-compose down -v
```

---

## Testing

The codebase features a robust automated test suite built with `pytest`. The tests are designed to ensure API reliability, data integrity, and strict state isolation.

**Test Suite Highlights:**
* **End-to-End (E2E) API Testing:** Validates request/response cycles, HTTP status codes, and data filtering using FastAPI's `TestClient`.
* **In-Memory Database & Dependency Injection:** Utilizes an ephemeral `SQLite` in-memory database (`sqlite:///:memory:`) combined with FastAPI's `dependency_overrides` to completely isolate test data from the development and production environments.
* **State Isolation:** Implements `pytest` fixtures to automatically setup and teardown database states (drop/create tables and seed mock data) before every single test execution.

To execute the test suite locally:
```bash
pytest -v
```

---

## Developer Workflow

If you wish to contribute or modify the code without rebuilding the entire Docker image for every change, use the hybrid setup:

1. **Set up your environment variables:**
Copy the template file. The default values are already configured to connect to the local Docker database.
```bash
cp .env.example .env
```

2. **Spin up only the database container:**
```bash
docker-compose up -d db
```

3. **Run the API locally with hot-reload (requires local Python environment):**
```bash
uvicorn app.main:app --reload
```

4. **Run the manual extractor (if needed):**
```bash
python -m app.scripts.collector
```

---

## Project Structure

```text
job-market-analytics-api/
├── app/
│   ├── api/                
│   │   └── routes/         # API Routers (jobs.py)
│   ├── models/             # SQLAlchemy ORM Models (job.py)
│   ├── schemas/            # Pydantic validation schemas (job.py)
│   ├── scripts/            # ETL Pipeline logic (collector.py)
│   ├── services/           # Business logic (job_service.py)
│   ├── database.py         # SQLAlchemy engine management
│   └── main.py             # FastAPI application entry point
├── tests/                  
│   └── test_api.py         # Pytest suite for endpoints
├── .env.example            # Environment variables template
├── .gitignore              # Ignored files and directories
├── Dockerfile              # API container definition
├── docker-compose.yml      # Multi-container orchestration
├── LICENSE                 # MIT License terms
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```
