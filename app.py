import os
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import requests
import io, base64
import plotly.express as px
import plotly.io as pio
from extensions import db
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# ----------- MODEL -----------
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    company = db.Column(db.String(200))
    location = db.Column(db.String(200))
    link = db.Column(db.String(500))


# ----------- FETCH DATA (API) -----------
def fetch_live_jobs(query="Data Analyst", location="India", limit=10):
    print("🔍 Fetching jobs from LinkedIn API...")

    url = "https://jsearch.p.rapidapi.com/search"
    api_key = os.getenv("RAPIDAPI_KEY", "your_api_key_here")
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
    params = {"query": f"{query} {location}", "num_pages": 1}

    try:
        response = requests.get(url, headers=headers, params=params)
        print("🔎 Response Code:", response.status_code)

        if response.status_code != 200:
            print("❌ API Error:", response.text)
            return []

        data = response.json().get("data", [])
        print("✅ Jobs fetched:", len(data))

        if not data:
            print("⚠️ No job data returned.")
            return []

        # Clear old jobs and save new ones
        Job.query.delete()
        for job in data[:limit]:
            new_job = Job(
                title=job.get("job_title", "N/A"),
                company=job.get("employer_name", "N/A"),
                location=job.get("job_location", "N/A"),
                link=job.get("job_apply_link", "#")
            )
            db.session.add(new_job)
        db.session.commit()

        print("✅ Jobs saved to DB successfully.")
        return data

    except Exception as e:
        print("❌ Error while fetching jobs:", e)
        return []


# ----------- ANALYSIS FUNCTION -----------
def analyze_jobs():
    jobs = Job.query.all()
    if not jobs:
        return None, None, None,None

    df = pd.DataFrame([{
        "title": j.title,
        "company": j.company,
        "location": j.location
    } for j in jobs])

    total = len(df)
    top_companies = df['company'].value_counts().head(5)
    top_locations = df['location'].value_counts().head(5)
    top_roles = df['title'].value_counts().head(7)

    
    # --- Top Companies Chart ---
    fig1 = px.bar(
        x=top_companies.index,
        y=top_companies.values,
        title="Top Hiring Companies",
        labels={'x': 'Company', 'y': 'Number of Jobs'},
        color=top_companies.index,
    )
    fig1.update_layout(
        
        title_font=dict(size=22, color="#1a73e8"),
        font=dict(size=14, color="#333"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=50, r=50, t=80, b=120)
    )

    # --- Top Locations Chart ---
    fig2 = px.pie(
        values=top_locations.values,
        names=top_locations.index,
        title="Top Job Locations",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig2.update_layout(
        title_font=dict(size=22, color="#1a73e8"),
        font=dict(size=14, color="#333"),
        legend_title_text='Locations',
        legend=dict(x=0.8, y=0.5)
    )

    # --- Top Roles Chart ---
    fig3 = px.bar(
        x=top_roles.index,
        y=top_roles.values,
        title="Top Roles Being Hired For",
        labels={'x': 'Job Role', 'y': 'Number of Openings'},
        color=top_roles.index,
    )
    fig3.update_layout(

        title_font=dict(size=22, color="#1a73e8"),
        font=dict(size=14, color="#333"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=50, r=50, t=80, b=120)
    )

    # Convert to interactive HTML snippets
    graph1 = fig1.to_html(full_html=False, include_plotlyjs='cdn')
    graph2 = fig2.to_html(full_html=False, include_plotlyjs=False)
    graph3 = fig3.to_html(full_html=False, include_plotlyjs=False)

    return total, graph1, graph2, graph3


# ----------- ROUTE (SINGLE DASHBOARD) -----------
@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        fetch_live_jobs()

    total, graph1, graph2, graph3 = analyze_jobs()
    return render_template('dashboard.html',
                            total=total,
                            graph1=graph1,
                            graph2=graph2,
                            graph3=graph3)


# ----------- APP LAUNCH -----------
if __name__ == '__main__':
    with app.app_context():
        db.drop_all()      # optional – clears old schema
        db.create_all()    # recreates tables properly
    app.run(debug=True)
