import tkinter as tk
from tkinter import ttk, messagebox
from models import Shop

class StoreApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title('Shop Manager')
        self.root.geometry("700x600")

        self.cart = []
        self.shop = Shop()

        self.create_widgets()

    def create_widgets(self) -> None:
        tk.Label(self.root, text='Товары на складе').pack(pady=20)

        columns = ('id', 'name', 'price', 'stock')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')

        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Название')
        self.tree.heading('price', text='Цена')
        self.tree.heading('stock', text='Остаток')

        self.tree.column('id', width=50)
        self.tree.pack(fill=tk.X, padx=10)

        buy_frame = tk.LabelFrame(self.root, text='Оформить покупку')
        buy_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(buy_frame, text='ID товара:').grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = tk.Entry(buy_frame, width=10)
        self.entry_id.grid(row=0, column=1)

        tk.Label(buy_frame, text='Количество товара:').grid(row=0, column=2, padx=5, pady=5)
        self.entry_qty = tk.Entry(buy_frame, width=10)
        self.entry_qty.grid(row=0, column=3)

        staff_frame = tk.LabelFrame(self.root, text='Смена кассира')
        staff_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(staff_frame, text='Текущий продавец:').grid(row=0, column=0, padx=5)
        employees_data = self.shop.get_all_employees()

        self.employee_list = [f'{e[0]} - {e[1]} {e[2]}' for e in employees_data]
        self.staff_combo = ttk.Combobox(staff_frame, values=self.employee_list, state="readonly", width=30)
        self.staff_combo.grid(row=0, column=1, padx=5, pady=5)
        if self.employee_list:
            self.staff_combo.current(0)

        main_frame = tk.LabelFrame(self.root, text='Основные функции')
        main_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(buy_frame, text='Добавить в корзину', command=self.add_to_cart).grid(row=0, column=4, padx=5)
        tk.Button(main_frame, text='Показать корзину', command=self.show_cart).pack(pady=10)
        tk.Button(main_frame, text='ОФОРМИТЬ ЧЕК', command=self.finalize_purchase).pack(pady=10)
        tk.Button(main_frame, text='Получить дневной отчет', command=self.show_daily_report).pack(pady=10, padx=50)

    def add_to_cart(self) -> None:
        '''Добавление товара в корзину'''
        p_id = self.entry_id.get()
        qty = self.entry_qty.get()

        if not p_id or not qty:
            messagebox.showwarning('Ошибка', 'Заполните все поля')
            return

        if int(p_id) not in self.shop.get_all_product_ids():
            print(self.shop.get_all_product_ids())
            messagebox.showwarning('Ошибка', 'Такого товара нет!')
            return

        else:
            self.cart.append((int(p_id), int(qty)))
            messagebox.showinfo('Корзина', f'Товар {p_id} добавлен. Всего позиций: {len(self.cart)}')
            self.entry_id.delete(0, tk.END)
            self.entry_qty.delete(0, tk.END)
            self.load_data()

    def finalize_purchase(self) -> None:
        '''Передача данных из корзины в базу данных для официального оформления чека и списания остатков'''
        if not self.cart:
            messagebox.showwarning('Ошибка', 'Корзина пуста')
            return

        cashier_id = self.get_selected_cashier_id()
        success, result = self.shop.make_purchase(cashier_id, self.cart)

        if success:
            str_cart = self.get_cart_list()
            messagebox.showinfo('Успех', f'Чек №{result} оформлен ({len(self.cart)}шт)\n{str_cart}')
            self.cart = []
            self.load_data()
        else:
            messagebox.showerror('Ошибка', f'Проблема при оформлении: {result}')

    def get_cart_list(self) -> str:
        '''Преобразование списка товаров по их id в красивую строку'''
        str_cart = ''
        for p_id, qty in self.cart:
            str_cart += f'{self.shop.get_product_by_id(p_id)[1]} - {qty} шт.\n'
        return str_cart

    def load_data(self) -> None:
        '''Обновление таблицы товаров'''
        for i in self.tree.get_children():
            self.tree.delete(i)

        for product in self.shop.get_all_products():
            self.tree.insert('', tk.END, values=product)

    def show_cart(self) -> None:
        '''Показать содержимое корзины'''
        if not self.cart:
            messagebox.showinfo('Корзина', 'Ваша корзина пока пуста')
            return
        str_cart = self.get_cart_list()
        messagebox.showinfo('Ваша корзина', str_cart)

    def get_selected_cashier_id(self) -> int | None:
        '''Получение id выбранного кассира'''
        selection = self.staff_combo.get()
        if selection:
            return int(selection.split(" ")[0])
        return None

    def show_daily_report(self) -> None:
        '''Формирование отчета за день'''
        today = __import__('datetime').datetime.now().strftime("%Y-%m-%d")
        sales_data = self.shop.get_sales_by_date(today)

        if not sales_data:
            messagebox.showinfo('Дневной отчет', f'За {today} продаж не найдено')
            return

        report_text = f'ОТЧЕТ ПО ПРОДАЖАМ ЗА {today}\n' + '_' * 34 + '\n'

        grand_total = 0
        for name, qty, revenue in sales_data:
            report_text += f'{name} || {qty} шт. || {revenue} руб.\n'
            grand_total += revenue

        report_text.rjust(15)

        report_text += f'\nИТОГО ВЫРУЧКА: {grand_total} руб'
        messagebox.showinfo('Дневной отчет', report_text)

if __name__ == '__main__':
    root = tk.Tk()
    app = StoreApp(root)
    app.load_data()
    root.mainloop()


