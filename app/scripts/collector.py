import pandas as pd
from app.database import SessionLocal, engine, Base
from app.models.job import Job
from datetime import datetime

def extract_data():
    print("Starting data extraction...")
    raw_jobs = [
        {"title": "Python Developer", "company": "Tech Corp", "location": "Remote", "salary": "5000"},
        {"title": "Data Engineer", "company": "Data Inc", "location": "São Paulo", "salary": "7000"},
        {"title": "Machine Learning Engineer", "company": "AI Solutions", "location": "Remote", "salary": "8500"},
        {"title": "Backend Developer", "company": "Cloud Systems", "location": "Curitiba", "salary": "not informed"},
    ]
    df = pd.DataFrame(raw_jobs)
    return df

def transform_data(df):
    print("Starting data transformation...")
    df['salary'] = pd.to_numeric(df['salary'], errors='coerce').fillna(0.0)
    df['title'] = df['title'].str.strip().str.title()
    df['company'] = df['company'].str.strip()
    print("Transformation completed.")
    return df

def load_data(df):
    print("Starting data load to database...")
    db = SessionLocal()
    try:
        for _, row in df.iterrows():
            new_job = Job(
                title=row['title'],
                company=row['company'],
                location=row['location'],
                technology="Python",
                salary_min=float(row['salary']),
                salary_max=0,
                posted_at=datetime.now()
            )
            db.add(new_job)
        
        db.commit()
        print(f"Success: {len(df)} jobs saved to the database!")
    except Exception as e:
        print(f"Error loading data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Checking database structure...")
    Base.metadata.create_all(bind=engine)
    
    raw_df = extract_data()
    clean_df = transform_data(raw_df)
    load_data(clean_df)