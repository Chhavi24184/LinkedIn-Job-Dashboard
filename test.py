import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://jsearch.p.rapidapi.com/search"
api_key = os.getenv("RAPIDAPI_KEY", "your_api_key_here")
headers = {
    "x-rapidapi-key": api_key,
    "x-rapidapi-host": "jsearch.p.rapidapi.com"
}
params = {"query": "Software Engineer India", "num_pages": 1}

r = requests.get(url, headers=headers, params=params)
print(r.status_code)
print(len(r.json().get("data", [])))
