import os
from db.db_utils import fetch_no_claim_articles, set_claims, fetch_claims
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

API_KEY = os.getenv("OPEN_AI_KEY")
client = OpenAI(api_key = API_KEY)

def get_validity(claim, evidence):
    response = client.chat.completions.create(
        model = "gpt-4.1",
        messages = [
            {
                "role": "system", 
                "content": "You will be provided a claim and some evidence. You are to act as a fact-checker and determine the validity of the claim based on the evidence."
            },
            {
                "role": "user", 
                "content": f"""Claim: {claim}
                            Based on the sources listed below, is this claim supported by evidence? Please respond with one word: yes or no.

                            Here is the evidence you should use: 

                            {evidence}
                            """
            }
        ]
    )
    response = response.choices[0].message.content
    return response.lower()
    