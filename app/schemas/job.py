from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class JobBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    company: str = Field(..., min_length=2)
    location: str
    technology: str
    seniority: Optional[str] = None
    salary: Optional[float] = Field(None, ge=0)

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: int
    posted_at: datetime

    class Config:
        from_attributes = True