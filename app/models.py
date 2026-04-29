import sqlite3
from config import DB_NAME

class Shop:
    def __init__(self):
        self.name = DB_NAME

    def _execute_query(self, query, params = (), fetchall = False):
        '''Формирование запроса к бд'''
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetchall:
                return cursor.fetchall()
            conn.commit()

    def get_all_products(self):
        '''Получение полного списка товаров (ID, название, цена, остаток) для отображения в таблице'''
        query = "SELECT id_product, name_of_product, price, quantity_at_storage FROM products"
        return self._execute_query(query, fetchall=True)

    def get_all_employees(self):
        '''Загрузка списка всех сотрудников для возможности выбора кассира в интерфейсе'''
        query = "SELECT id, name, surname FROM employees"
        return self._execute_query(query, fetchall=True)

    def get_product_by_id(self, id_product):
        '''Получение конкретного товара по его id'''
        for product in self.get_all_products():
            if product[0] == id_product:
                return product
        return None

    def get_all_product_ids(self):
        '''Получение id всех товаров для проверки корректности введенного значения'''
        query = "SELECT id_product FROM products"
        return [int(i[0]) for i in self._execute_query(query, fetchall=True)]

    def make_purchase(self, id_cashier, cart_items):
        '''Главный метод оформления покупки: создание чека, списывание остатков, запись позиций'''
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

    def get_sales_by_date(self, date):
        '''Формирование отчета за выбранную дату'''
        query = '''
        SELECT products.name_of_product, SUM(sale_items.quantity), SUM(sale_items.quantity * products.price)
        FROM sale_items
        JOIN receipts ON sale_items.id_check = receipts.id_check
        JOIN products ON sale_items.id_product = products.id_product
        WHERE DATE(receipts.created_at) = ?
        GROUP BY products.id_product
        '''
        return self._execute_query(query, params=(date, ), fetchall=True)






