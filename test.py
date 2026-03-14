import requests

url = "https://jsearch.p.rapidapi.com/search"
headers = {
    "x-rapidapi-key": "ba99c87b71msh82db2b7dbb6ee00p160458jsn10b67a0946c3",
    "x-rapidapi-host": "jsearch.p.rapidapi.com"
}
params = {"query": "Software Engineer India", "num_pages": 1}

r = requests.get(url, headers=headers, params=params)
print(r.status_code)
print(len(r.json().get("data", [])))
