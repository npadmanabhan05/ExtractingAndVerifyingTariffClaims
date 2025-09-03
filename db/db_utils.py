import sqlite3, csv

# this file will hold any functions that execute operations related to the database (creating the database, inserting an article, etc.)

def getConnection():
    return sqlite3.connect('db/articles.db')

def create_articles_table():
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
            supported_claims TEXT,
            num_supported_claims INTEGER,
            is_fact_checked INTEGER DEFAULT 0
        )
    ''')
    connection.commit()
    connection.close()

def create_economic_data_table():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS economic_data (
            research_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            title TEXT,
            authors TEXT,
            source TEXT,
            content TEXT,
            in_pinecone INTEGER DEFAULT 0
        )
    ''')
    connection.commit()
    connection.close()

def insert_articles(data, political_leaning):
    # retreives an list of dictionaries representing the various articles returned by the News API
    articles = data.get("articles", [])
    # checks if any articles were returned
    if not articles: 
        print("no articles found")
        return
    connection = getConnection()
    cursor = connection.cursor()
    # attemps to insert each article into the database
    for article in articles: 
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO articles(
                    timestamp, title, author, description, url, 
                    source, political_affiliation, claims, num_claims, 
                    assumptions, num_assumptions, supported_claims, num_supported_claims, is_fact_checked
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
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

def insert_economic_data(data):
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT exists (SELECT 1 FROM economic_data WHERE content = ?)", (data.get("content"),))
    if (cursor.fetchone()[0]== 0):
        cursor.execute('''
            INSERT OR IGNORE INTO economic_data(
                date, title, authors, source, content, in_pinecone
            ) VALUES (?, ?, ?, ?, ?, ?)''', 
            (
                data.get("date"),
                data.get("title"),
                data.get("authors"),
                data.get("source"),
                data.get("content"),
                0
            )
        )
    connection.commit()
    connection.close()

def fetch_unadded_economic_data():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT research_id, date, title, authors, source, content FROM economic_data WHERE in_pinecone = ?", (0,))
    data = cursor.fetchall()
    connection.commit()
    connection.close()
    return data

def fetch_all_economic_data():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT title FROM economic_data")
    rows = cursor.fetchall()
    print(len(rows))
    with open('exported_economic_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title"])
        for row in rows:
            writer.writerow(row)
    print(f"Exported {len(rows)} papers to exported_economic_data.csv")
    connection.commit()
    connection.close()

# to check if everything is being added correctly
def fetch_all_article_claims():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT article_id, claims FROM articles WHERE political_affiliation=? OR political_affiliation=?", ("Left", "Center-Left"))
    rows = cursor.fetchall()
    with open('exported_claims_left.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Article ID", "Claims"])
        for row in rows:
            writer.writerow([row[0], row[1]])
    cursor.execute("SELECT article_id, claims FROM articles WHERE political_affiliation=?", ("Center",))
    rows = cursor.fetchall()
    with open('exported_claims_center.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Article ID", "Claims"])
        for row in rows:
            writer.writerow([row[0], row[1]])
    cursor.execute("SELECT article_id, claims FROM articles WHERE political_affiliation=? OR political_affiliation=?", ("Right", "Center-Right"))
    rows = cursor.fetchall()
    with open('exported_claims_right.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Article ID", "Claims"])
        for row in rows:
            writer.writerow([row[0], row[1]])
    print(f"Exported {len(rows)} claims")
    connection.commit()
    connection.close()

def fetch_all_article_facts():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT supported_claims FROM articles WHERE political_affiliation=? OR political_affiliation=?", ("Left", "Center-Left"))
    rows = cursor.fetchall()
    with open('exported_facts_left.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow("Supported Claims")
        for row in rows:
            writer.writerow(row)
    cursor.execute("SELECT supported_claims FROM articles WHERE political_affiliation=?", ("Center",))
    rows = cursor.fetchall()
    with open('exported_facts_center.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow("Supported Claims")
        for row in rows:
            writer.writerow(row)
    cursor.execute("SELECT supported_claims FROM articles WHERE political_affiliation=? OR political_affiliation=?", ("Right", "Center-Right"))
    rows = cursor.fetchall()
    with open('exported_facts_right.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow("Supported Claims")
        for row in rows:
            writer.writerow(row)
    print(f"Exported {len(rows)} facts")
    connection.commit()
    connection.close()

def fetch_all_article_assumptions():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT assumptions FROM articles WHERE political_affiliation=? OR political_affiliation=?", ("Left", "Center-Left"))
    rows = cursor.fetchall()
    with open('exported_assumptions_left.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow("Assumptions")
        for row in rows:
            writer.writerow(row)
        print(f"exported {len(rows)} articles")
    cursor.execute("SELECT assumptions FROM articles WHERE political_affiliation=?", ("Center",))
    rows = cursor.fetchall()
    with open('exported_assumptions_center.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow("Assumptions")
        for row in rows:
            writer.writerow(row)
    cursor.execute("SELECT assumptions FROM articles WHERE political_affiliation=? OR political_affiliation=?", ("Right", "Center-Right"))
    rows = cursor.fetchall()
    with open('exported_assumptions_right.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow("Assumptions")
        for row in rows:
            writer.writerow(row)
    print(f"Exported {len(rows)} assumptions")
    connection.commit()
    connection.close()

def fetch_no_claim_articles():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT article_id, content from articles WHERE claims IS NULL AND content IS NOT NULL")
    unchecked_articles = cursor.fetchall()
    if not unchecked_articles: 
        print("None")
    connection.commit()
    connection.close()
    return unchecked_articles
    

def add_content(id, content):
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute('''
       UPDATE articles
       SET content = ?
       WHERE article_id = ?
    ''', (content, id))
    connection.commit()
    connection.close()

def set_claims(id, claims):
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE articles
        SET claims = ?
        WHERE article_id = ?
    ''', (claims, id))
    connection.commit()
    connection.close()

def set_assumptions(id, assumptions, num_assumptions): 
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE articles
        SET assumptions = ?,
            num_assumptions = ?
        WHERE article_id = ?;
    ''', (assumptions, num_assumptions, id))
    connection.commit()
    connection.close()

def set_supported_claims(id, facts, num_supported_claims): 
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE articles
        SET supported_claims = ?,
            num_supported_claims = ?
        WHERE article_id = ?;
    ''', (facts, num_supported_claims, id))
    connection.commit()
    connection.close()

def declare_as_fact_checked(id):
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE articles
        SET is_fact_checked = ?
        WHERE article_id = ?;
    ''', (1, id))
    connection.commit()
    connection.close()

def fetch_claims(id):
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT claims FROM articles WHERE article_id = ?
    ''', (id,))
    claims = cursor.fetchone()
    connection.commit()
    connection.close()
    return claims

def mark_as_added_to_pinecone(research_id):
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE economic_data
        SET in_pinecone = ?
        WHERE research_id = ?
    ''', (1, research_id))
    connection.commit()
    connection.close()

def fetch_unchecked_articles():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT article_id, claims FROM articles WHERE is_fact_checked = ? AND claims IS NOT NULL", (0,))
    articles = cursor.fetchall()
    connection.commit()
    connection.close()
    return articles

def fetch_economic_info(id):
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT content FROM economic_data WHERE research_id = ?", (id,))
    text = cursor.fetchone()
    return text[0] if text else ""
