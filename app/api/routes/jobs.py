from fastapi import APIRouter

router = APIRouter()

@router.get("/jobs")
def get_jobs():
    return [
        {"title": "Backend Developer", "language": "Python"},
        {"title": "Data Engineer", "language": "Python"},
        {"title": "Frontend Developer", "language": "JavaScript"}
    ]