from news_scraping.scrape import get_articles
from db.db_utils import fetch_all_articles

# adding articles form left-leaning news publications
#get_articles("theguardian.com", "Left")
get_articles("the-huffington-post,associated-press,buzzfeed,msnbc,new-york-magazine", "Left")
#get_articles("vox.com", "Left")

# # adding articles form center-left-leaning news publications
# get_articles("npr.org", "Center-Left")
# get_articles("politico.com", "Center-Left")
# get_articles("newsweek.com", "Center-Left")

# # adding articles form center news publications
# get_articles("reuters.com", "Center")
# get_articles("bbc.com", "Center")
# get_articles("abcnews.go.com", "Center")

# # adding articles form center-right-leaning news publications
# get_articles("thehill.com", "Center-Right")
# get_articles("washingtonexaminer.com", "Center-Right")
# get_articles("foxbusiness.com", "Center-Right")

# # adding articles form right-leaning news publications
# get_articles("foxnews.com", "Right")
# get_articles("breitbart.com", "Right")
# get_articles("dailywire.com", "Right")

# #fetching the articles to make sure that everything was added properly 
fetch_all_articles()
