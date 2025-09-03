from news_scraping.scrape import get_articles
from db.db_utils import fetch_all_articles

# adding articles form left-leaning news publications
get_articles("the-huffington-post,associated-press,buzzfeed,msnbc,new-york-magazine", "Left")

# adding articles form center-left-leaning news publications
 get_articles("abc-news,cnn,time,nbc-news", "Center-Left")

# # adding articles form center news publications
get_articles("bbc-news,reuters", "Center")

# # adding articles form center-right-leaning news publications
get_articles("national-review,the-washington-times,the-hill", "Center-Right")

# # adding articles form right-leaning news publications
 get_articles("fox-news,breitbart-news,the-american-conservative", "Right")

# #fetching the articles to make sure that everything was added properly 
fetch_all_articles()
