import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

from app.main import app
from app.database import Base, get_db
from app.models.job import Job

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    job1 = Job(
        title="Python Developer", company="Test Corp", location="Remote",
        technology="Python", seniority="Mid", salary=5000.0, posted_at=datetime.now(timezone.utc)
    )
    job2 = Job(
        title="Java Engineer", company="Enterprise LLC", location="NY",
        technology="Java", seniority="Senior", salary=8000.0, posted_at=datetime.now(timezone.utc)
    )
    db.add(job1)
    db.add(job2)
    db.commit()
    db.close()

def test_list_jobs_with_filter():
    response = client.get("/jobs?tech=Python")
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    assert "Python" in data[0]["technology"]

def test_statistics_endpoint():
    response = client.get("/jobs/stats")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "success"
    assert data["data"]["overview"]["total_jobs"] == 2