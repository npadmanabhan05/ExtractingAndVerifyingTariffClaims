# basic setup of the databse (to be ran once)

from db.db_utils import create_articles_table, create_economic_data_table, temp, fetch_unadded_economic_data
# create_articles_table()
# create_economic_data_table()
# temp()
print(fetch_unadded_economic_data())