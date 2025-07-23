import os, requests, json, urllib.request
from dotenv import load_dotenv
from db.db_utils import insert_articles

load_dotenv()

#API_KEY = os.getenv("GNEWS_API_KEY")

API_KEY = os.getenv("NEWS_API_KEY")

def get_articles(sites, political_leaning):
    url = f"https://newsapi.org/v2/top-headlines?pageSize=50&page=1&sources={sites}&q=tariff&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    insert_articles(data, political_leaning)
