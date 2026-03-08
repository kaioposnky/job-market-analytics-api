from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Job Market API running"}

@app.get("/jobs")
def get_jobs():
    return [
        {"title": "Backend Developer", "language": "Python"},
        {"title": "Data Engineer", "language": "Python"},
        {"title": "Frontend Developer", "language": "JavaScript"}
    ]
