import sqlite3
from config import DB_NAME

class Shop:
    def __init__(self):
        self.name = __import__('os').path.join('shop_app', DB_NAME)

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

    def make_purchase(self, id_cashier, cart_items):
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")

            try:
                cursor.execute('''INSERT INTO receipts (id_cashier) VALUES (?)''', (id_cashier,))
                id_check = cursor.lastrowid

                for id_product, quantity in cart_items:
                    cursor.execute("SELECT quantity_at_storage FROM products WHERE id_product = ?", (id_product,))
                    stock = cursor.fetchone()[0]

                    if stock < quantity:
                        raise ValueError(f"Недостаточно товара {id_product} на складе")

                    cursor.execute('''UPDATE products SET quantity_at_storage = ? WHERE id_product = ?''', (stock - quantity, id_product))
                    cursor.execute('''INSERT INTO sale_items (id_check, id_product, quantity) VALUES (?, ?, ?)''', (id_check, id_product, quantity))

                conn.commit()
                return True, id_check

            except Exception as e:
                conn.rollback()
                return False, e






