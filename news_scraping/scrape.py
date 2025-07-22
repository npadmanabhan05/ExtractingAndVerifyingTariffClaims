import os, requests, json, urllib.request
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GNEWS_API_KEY")
category = "general"
q = "tariffs"
domain = "reuters.com"
language = "en"
max_results = 10

def get_articles(site_domain)
    domain = site_domain
    url = (
    f"https://gnews.io/api/v4/search"
    f"?q={q}"
    f"&site={domain}"
    f"&lang={language}"
    f"&max={max_results}"
    f"&token={API_KEY}"
    )
    response = requests.get(url)
    data = response.json()
    return data
