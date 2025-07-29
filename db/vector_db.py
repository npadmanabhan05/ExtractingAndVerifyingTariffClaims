import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from db.db_utils import mark_as_added_to_pinecone

load_dotenv()

API_KEY = os.getenv("PINECONE_API_KEY")
# pinecone.init(api_key=API_KEY, environment="us-east-1-aws")
pc = Pinecone(api_key=API_KEY)
index_name = "economic-information"

pc.create_index(
    name = index_name,
    dimension = 1536,
    metric = "cosine",
    spec = ServerlessSpec(cloud = "aws", region = "us-east-1")
)

def add_to_pinecone(data, embedding):
    global id
    index = pc.Index("economic-information")
    index.upsert([
        {
            "id": data.get("research_id"),
            "values" : embedding,
            "metadata": {
                "title" : data.get("title")
            }
        }
    ])
    mark_as_added_to_pinecone(data.get("research_id"))

