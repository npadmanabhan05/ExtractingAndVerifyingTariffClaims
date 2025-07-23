import sqlite3, csv


# this file will hold any functions that execute operations related to the database (creating the database, inserting an article, etc.)

def getConnection():
    return sqlite3.connect('db/articles.db')

def create_table():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            article_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            title TEXT,
            author TEXT,
            description TEXT,
            url TEXT,
            source TEXT,
            political_affiliation TEXT,
            claims TEXT,
            num_claims INTEGER,
            assumptions TEXT,
            num_assumptions INTEGER,
            is_fact_checked INTEGER DEFAULT 0
        )
    ''')
    connection.commit()
    connection.close()

def insert_articles(data, political_leaning):
    # retreives an list of dictionaries representing the various articles returned by the GNews API
    articles = data.get("articles", [])
    if not articles: 
        print("no articles found")
        return
    connection = getConnection()
    cursor = connection.cursor()
    for article in articles: 
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO articles(
                    timestamp, title, author, description, url, 
                    source, political_affiliation, claims, num_claims, 
                    assumptions, num_assumptions, is_fact_checked
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (
                    article.get("publishedAt"),
                    article.get("title"),
                    article.get("author"),
                    article.get("description"),
                    article.get("url"),
                    article.get("source", {}).get("name", ""),
                    political_leaning, 
                    None, 
                    None, 
                    None, 
                    None, 
                    0
                )
            )
        except Exception as e:
            print(f"Error inserting article: {article.get('title')}\n{e}")
    connection.commit()
    connection.close()
    print(f"Inserted {len(articles)} articles. Duplicates skipped")

# to check if everything is being added correctly
def fetch_all_articles():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT title, url, source, political_affiliation FROM articles")
    rows = cursor.fetchall()
    with open('exported_articles.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Url", "Source", "Political Affiliation"])

        for row in rows:
            writer.writerow(row)
    print(f"Exported {len(rows)} articles to exported_articles.csv")
