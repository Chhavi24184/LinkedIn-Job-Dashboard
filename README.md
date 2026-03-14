# LinkedIn Job Dashboard

A Flask-based web application to fetch live job listings from LinkedIn using RapidAPI and visualize the data with interactive charts.

## Features
- **Live Job Fetching**: Pulls the latest job listings for specific roles and locations.
- **Data Visualization**: Interactive charts using Plotly (Top Companies, Locations, and Roles).
- **SQLite Database**: Stores job data locally using Flask-SQLAlchemy.
- **Clean UI**: Responsive dashboard with job links.

## Tech Stack
- **Backend**: Flask, Flask-SQLAlchemy
- **Data Handling**: Pandas
- **Visualization**: Plotly, Matplotlib
- **Frontend**: HTML, CSS, JavaScript (via Jinja2 templates)
- **API**: JSearch (RapidAPI)

## Getting Started

### Prerequisites
- Python 3.10+
- RapidAPI Key (JSearch API)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Chhavi24184/LinkedIn-Job-Dashboard.git
   cd LinkedIn-Job-Dashboard
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your API key in `app.py`:
   ```python
   headers = {
       "x-rapidapi-key": "YOUR_REAL_KEY",
       "x-rapidapi-host": "jsearch.p.rapidapi.com"
   }
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open your browser to `http://127.0.0.1:5000/`.

## License
MIT License
