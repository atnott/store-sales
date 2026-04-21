import sqlite3
from config import DB_NAME, queries

def create_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        for query in queries:
            cursor.execute(query)
        conn.commit()

def load_from_file(file_path, query):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        with open(file_path, 'r', encoding='utf-8') as file:
            data = []
            for line in file:
                row = tuple(el.strip() for el in line.split(','))
                data += [row]
            cursor.executemany(query, data)
        conn.commit()

if __name__ == '__main__':
    create_db()
    load_from_file('data/categories.txt',"INSERT INTO categories (name_category) VALUES (?)")
    load_from_file('data/products.txt',"INSERT INTO products (name_of_product, price, id_category, quantity_at_storage) VALUES (?, ?, ?, ?)")
    load_from_file('data/jobs_titles.txt', "INSERT INTO jobs_titles (name) VALUES (?)")
    load_from_file('data/employees.txt', "INSERT INTO employees (name, surname, id_job_title) VALUES (?, ?, ?)")