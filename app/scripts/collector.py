import pandas as pd
from app.database import SessionLocal, engine, Base
from app.models.job import Job
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def extract_data():
    print("Starting real data extraction from Python.org...")
    url = "https://www.python.org/jobs/"
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    raw_jobs = []
    
    job_container = soup.find("ol", class_="list-recent-jobs")
    
    if job_container:
        jobs = job_container.find_all("li")
        
        for job in jobs:
            title_tag = job.find("h2").find("a")
            title = title_tag.text.strip() if title_tag else "No Title"
            
            company_tag = job.find("span", class_="listing-company-name")
            if company_tag:
                company = company_tag.text.replace("New", "").strip().split('\n')[-1].strip()
            else:
                company = "Unknown"
                
            location_tag = job.find("span", class_="listing-location")
            location = location_tag.text.strip() if location_tag else "Remote"
            
            raw_jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "salary": "0" 
            })
            
    df = pd.DataFrame(raw_jobs)
    print(f"Success! {len(df)} jobs extracted from the web.")
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