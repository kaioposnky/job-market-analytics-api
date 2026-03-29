from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.database import engine, Base
from app.api.routes import jobs_router

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Jobs Data",
        "description": "Endpoints to query and filter raw job listings.",
    },
    {
        "name": "Market Statistics",
        "description": "Aggregated analytics and insights about the tech job market.",
    },
    {
        "name": "Infrastructure",
        "description": "System health and status checks.",
    }
]

description = """
An analytical API designed to extract, clean, and provide insights on the Tech Job Market. 🚀

### 📊 Core Features
* **Job Explorer:** Filter opportunities by technology, seniority, location, and company.
* **Market Intelligence:** Access aggregated metrics on remote work trends, top technologies, and hiring companies.

*Powered by Python, FastAPI, and PostgreSQL.*
"""

app = FastAPI(
    title="Job Market Analytics API",
    description=description,
    version="1.0.0",
    openapi_tags=tags_metadata,
    contact={
        "name": "GitHub Repository",
        "url": "https://github.com/abreu-joao/job-market-api",
    }
)

print("\nAPI in on! Access: http://localhost:8000\n", flush=True)

@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["Infrastructure"])
def health_check():
    return {"status": "online", "database": "connected"}

app.include_router(jobs_router)