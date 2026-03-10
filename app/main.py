from fastapi import FastAPI
from app.database import engine, Base
from app.models import job
from app.api.routes import jobs

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Market API")

@app.get("/")
def home():
    return {"message": "Job Market API running and Database Connected"}

app.include_router(jobs.router)