import sqlite3
from config import DB_NAME, queries

def create_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        for query in queries:
            cursor.execute(query)

if __name__ == '__main__':
    create_db()