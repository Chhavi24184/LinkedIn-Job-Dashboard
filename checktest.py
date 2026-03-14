import requests
import json

url = "https://jsearch.p.rapidapi.com/search"
headers = {
    "x-rapidapi-key": "ba99c87b71msh82db2b7dbb6ee00p160458jsn10b67a0946c3",   # paste your actual key
    "x-rapidapi-host": "jsearch.p.rapidapi.com"
}
params = {"query": "data analyst in india", "num_pages": 1}

r = requests.get(url, headers=headers, params=params)
print("Status:", r.status_code)

data = r.json()
# Print only one sample job record, nicely formatted
print(json.dumps(data["data"][0], indent=4))
