import os
from db.db_utils import fetch_no_claim_articles, set_claims, fetch_claims
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

API_KEY = os.getenv("OPEN_AI_KEY")
client = OpenAI(api_key = API_KEY)
# articles here is a list of various tuples that represent the individual articles
articles = fetch_no_claim_articles()
for article in articles: 
    id = article[0]
    text = article[1]
    response = client.chat.completions.create(
        model = "gpt-4.1",
        messages = [
            {
                "role": "system", 
                "content": "You are an economic-claim extractor. Please only extract economic claims made by the author of the article. Avoid refrencing quotes from the president or other individuals"
            },
            {
                "role": "user", 
                "content": f"""From the following article, can you extract all of the claims that the author or the news outlet itself makes about tariffs or the economy. These claims should cover areas such as the current state of the economy, the effects of tariffs, etc. Please focus on the claims made by the author or news outlet and avoid claims made about what trump or other officials are saying. Please provide me a list of claims (as a list of strings). This is how the output should look: 

                            [
                                claim 1,
                                claim 2,
                                etc.
                            ]
                            If there are no economic claims made, please output the following empty list: []
                            Here is the article: 

                                {text}
                            """
            }
        ]
    )
    claims = response.choices[0].message.content
    set_claims(id, claims)

