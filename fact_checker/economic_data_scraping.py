import os, requests, json, fitz
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPEN_AI_KEY")
client = OpenAI(api_key = OPENAI_API_KEY)
CORE_API_KEY = os.getenv("CORE_API_KEY")

# for statistical data
def get_world_bank_data(indicators): 
    indicator_data = {}
    for key in indicators: 
        url = f"https://api.worldbank.org/v2/country/US/indicator/{indicators[key]}?date=2018:2025&format=json"
        response = requests.get(url)
        stat_data = response.json()
        # converting the given response to simple text
        response = client.chat.completions.create(
            model = "gpt-4.1",
            messages = [
                {
                    "role" : "system",
                    "content" : "You are to convert Json data that represents economic indicators to plain text. Only output a paragraph of text"
                },
                {
                    "role" : "user",
                    "content" :  f""" Convert the following World Bank JSON data into plain English sentences. Each sentence should state the {key} of the United States for the given year in the format:
                              "The United States {key} in [year] was [$value]."
                              Please also give me sentences saying:
                              "The United States {key} grew [some growth percentage based off the numbers] in [year]." 
                              Here is the JSON data: 
                              {json.dumps(stat_data)}
                    
                            """
                }
            ]
        )
        text_representation = response.choices[0].message.content
        indicator_data[key] = text_representation
    return indicator_data


# for economic reserch papers
def get_economic_research_full_text(params):
    url = f"https://api.core.ac.uk/v3/search/works?"
    headers = {
        "Authorization" : f"Bearer {CORE_API_KEY}"
    }
    response = requests.get(url, headers = headers, params = params)
    if (response.status_code != 200) :
        return "no params", None
    economic_research = response.json()
    params = {
        "scrollId" : economic_research.get("scrollId")
    }
    if (economic_research is None) :
        return params, None
    return params, economic_research.get("results")


# used to convert the json formatted responses from the other apis to simple text that can easily be embedded 

def get_pdf_text(file):
    try:
        doc = fitz.open(file)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        return full_text
    except Exception as e:
        print(f"An error occured: {e}")

