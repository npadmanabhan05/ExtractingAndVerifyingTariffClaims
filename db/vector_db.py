import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from db.db_utils import mark_as_added_to_pinecone

load_dotenv()

API_KEY = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=API_KEY)
index_name = "economic-information"
index = pc.Index("economic-information")

def add_to_pinecone(data, embedding):
    index.upsert([
        {
            "id": f"{data[0]}", # research id
            "values" : embedding,
            "metadata": {
                "title" : data[2] # title
            }
        }
    ])
    mark_as_added_to_pinecone(data[0])

def get_relevant_info(embedding):
    results = index.query(
        vector = embedding,
        top_k = 3,
        namespace = "__default__",
    )
    return results.get('matches')

