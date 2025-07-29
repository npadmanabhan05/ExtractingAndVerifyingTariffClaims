import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPEN_AI_KEY")
client = OpenAI(api_key = API_KEY)

def get_embedding(text):
    response = client.embeddings.create(
        input = text,
        model = "text-embedding-3-small"
    )

    embedding = response.data[0].embedding
    return embedding
