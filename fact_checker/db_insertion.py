from fact_checker.economic_data_scraping import get_world_bank_data, get_economic_research_full_text
from fact_checker.embedding_creation import get_embedding
from db.db_utils import insert_economic_data
import tiktoken,json

encoding = tiktoken.get_encoding("cl100k_base")

def token_chunker(text):
    tokenized_text = encoding.encode(text)
    current_chunk = []
    chunks = []
    index = 0
    while (index < len(tokenized_text)):
        if (len(current_chunk) <  8,000):
            current_chunk.append(tokenized_text[index])
            index = index + 1
        else :
            chunks.append(encoding.decode(current_chunk))   
            current_chunk = []
    if (len(current_chunk) > 0):
        chunks.append(encoding.decode(current_chunk))
    return chunks

# indicators = {
#     "GDP" : "NY.GDP.MKTP.CD",
#     "CPI" : "FP.CPI.TOTL.ZG",
#     "Unemployment rate" : "SL.UEM.TOTL.ZS",
#     "GNI per capita" : "NY.GNP.PCAP.CD"
#     }

# # inserting the statistical data into the database
# statistical_data = get_world_bank_data(indicators)
# statistical_data_text = ""
# for key in statistical_data: 
#     statistical_data_text = statistical_data_text + statistical_data[key] + "\n"
# statistical_data = {
#     "title" : "economic statistics", 
#     "date" : "2018-2025",
#     "authors" : "N/A",
#     "source" : "World Bank",
#     "content" : statistical_data_text
# }
# insert_economic_data(statistical_data)

# inserting the economic research papers into the database 
economic_research_full_text = get_economic_research_full_text()
for result in economic_research_full_text: 
    text = "Abstract: \n\n" + result.get("abstract") + "\n\n" + "Full text: \n\n" + result.get("fullText") 
    chunks = []
    if (len(encoding.encode(text)) < 8000):
        chunks.append(text)
    else:
        chunks = token_chunker(text)
    for chunk in chunks:
        research_info = {
            "title" : result.get("title"),
            "date" : result.get("createdDate"),
            "authors" : json.dumps(result.get("authors")),
            "source" : result.get("publisher"),
            "content" : chunk
        }
        insert_economic_data(research_info)


        
