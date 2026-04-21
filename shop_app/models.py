import sqlite3
from config import DB_NAME

class Shop:
    def __init__(self):
        self.name = DB_NAME

    def _execute_query(self, query, params = (), fetchall = False):
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetchall:
                return cursor.fetchall()
            conn.commit()

    def get_all_products(self):
        query = "SELECT id_product, name_of_product, price, quantity_at_storage FROM products"
        return self._execute_query(query, fetchall=True)

    def get_all_employees(self):
        query = "SELECT id, name, surname FROM employees"
        return self._execute_query(query, fetchall=True)