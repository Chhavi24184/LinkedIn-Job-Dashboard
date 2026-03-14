import requests
import pandas as pd
from extensions import db

def fetch_linkedin_jobs(query="Data Analyst", location="India"):
    """
    Fetches LinkedIn job data using RapidAPI and saves it to the database + CSV.
    """
    # ✅ Import here to avoid circular dependency
    from app import Job

    url = "https://linkedin-data-api.p.rapidapi.com/search-jobs"
    headers = {
        "x-rapidapi-key": "ba99c87b71msh82db2b7dbb6ee00p160458jsn10b67a0946c3",  # replace with your key or .env variable
        "x-rapidapi-host": "linkedin-data-api.p.rapidapi.com"
    }
    params = {"keywords": query, "location": location, "limit": 10}

    print("🔍 Fetching jobs from LinkedIn API...")

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json().get("data", [])
        jobs = []

        for job in data:
            job_entry = {
                "title": job.get("title"),
                "company": job.get("companyName"),
                "location": job.get("location"),
                "posted": job.get("listedAt"),
                "link": job.get("jobUrl")
            }
            jobs.append(job_entry)

            # ✅ Save to DB
            new_job = Job(
                title=job_entry["title"],
                company=job_entry["company"],
                location=job_entry["location"],
                link=job_entry["link"]
            )
            db.session.add(new_job)

        db.session.commit()

        df = pd.DataFrame(jobs)
        df.to_csv("latest_jobs.csv", index=False)

        print(f"✅ {len(jobs)} jobs fetched and saved to DB + CSV.")
        return df

    else:
        print(f"❌ Error fetching data: {response.status_code}")
        return pd.DataFrame()
