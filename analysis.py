import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def generate_analysis():
    """Generate insights and a plot from the LinkedIn job database."""

    # ✅ Import here (lazy import to avoid circular dependency)
    from extensions import db
    from app import Job

    # Get data from DB
    jobs = Job.query.all()
    if not jobs:
        return {
            "total_jobs": 0,
            "top_companies": {},
            "top_locations": {},
            "plot_url": ""
        }

    # Convert jobs to DataFrame
    df = pd.DataFrame([{
        "title": j.title,
        "company": j.company,
        "location": j.location,
        "link": j.link
    } for j in jobs])

    total_jobs = len(df)
    top_companies = df['company'].value_counts().head(5).to_dict()
    top_locations = df['location'].value_counts().head(5).to_dict()

    # Generate a static bar chart
    plt.figure(figsize=(6, 4))
    df['company'].value_counts().head(5).plot(kind='bar', color='skyblue')
    plt.title("Top Hiring Companies")
    plt.xlabel("Company")
    plt.ylabel("Job Count")

    # Convert plot to base64
    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return {
        "total_jobs": total_jobs,
        "top_companies": top_companies,
        "top_locations": top_locations,
        "plot_url": plot_url
    }
