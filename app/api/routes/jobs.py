from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobResponse, JobCreate

router = APIRouter()

@router.get("/jobs", response_model=List[JobResponse])
def read_jobs(db: Session = Depends(get_db)):

    jobs = db.query(Job).all()
    return jobs

@router.post("/jobs", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):

    new_job = Job(
        title=job.title,
        company=job.company,
        location=job.location,
        technology=job.technology,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        description=job.description
    )
    
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    
    return new_job