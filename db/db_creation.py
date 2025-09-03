# basic setup of the databse (to be ran once)
from db.db_utils import create_articles_table, create_economic_data_table
from db.pinecone_creation import create_pinecone_index
create_articles_table()
create_economic_data_table()
create_pinecone_index("economic-information")



