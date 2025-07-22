import sqlite3

# this file will hold any functions that execute operations related to the database (creating the database, inserting an article, etc.)

def getConnection():
    return sqlite3.connect('articles.db')

def create_table():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            article_id TEXT PRIMARY KEY,
            timestamp TEXT,
            title TEXT,
            author TEXT,
            description TEXT,
            url TEXT,
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