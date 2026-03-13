import pandas as pd

def extract_data():
    #Simulates data extraction from a raw source
    print("Starting data extraction...")
    
    raw_jobs = [
        {"title": "Python Developer", "company": "Tech Corp", "location": "Remote", "salary": "5000"},
        {"title": "Data Engineer", "company": "Data Inc", "location": "São Paulo", "salary": "7000"},
        {"title": "Machine Learning Engineer", "company": "AI Solutions", "location": "Remote", "salary": "8500"},
        {"title": "Backend Developer", "company": "Cloud Systems", "location": "Curitiba", "salary": "not informed"},
    ]
    
    df = pd.DataFrame(raw_jobs)
    return df

if __name__ == "__main__":
    df = extract_data()
    print("\n--- Extracted Data ---")
    print(df)