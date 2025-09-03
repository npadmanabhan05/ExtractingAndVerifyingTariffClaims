from db.db_utils import fetch_unadded_economic_data
from db.vector_db import add_to_pinecone
from fact_checker.embedding_creation import get_embedding

results = fetch_unadded_economic_data()

for result in results:
    embedding = get_embedding(result[5])
    add_to_pinecone(result, embedding)