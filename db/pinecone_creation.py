import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=API_KEY)
def create_pinecone_index(index_name):
    pc.create_index(
        name = index_name,
        dimension = 1536,
        metric = "cosine",
        spec = ServerlessSpec(cloud = "aws", region = "us-east-1")
    )