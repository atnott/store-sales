import tkinter as tk
from tkinter import ttk, messagebox
from models import Shop

class StoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Shop Manager')
        self.root.geometry("700x500")

        self.cart = []

        self.shop = Shop()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text='Товары на складе').pack(pady=20)

        columns = ('id', 'name', 'price', 'stock')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')

        self.tree.heading('id', text='ID')
        self.tree.heading("name", text="Название")
        self.tree.heading("price", text="Цена")
        self.tree.heading("stock", text="Остаток")

        self.tree.column("id", width=50)
        self.tree.pack(fill=tk.X, padx=10)

        buy_frame = tk.LabelFrame(self.root, text="Оформить покупку")
        buy_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(buy_frame, text="ID товара:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = tk.Entry(buy_frame, width=10)
        self.entry_id.grid(row=0, column=1)

        tk.Label(buy_frame, text="Количество товара:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_qty = tk.Entry(buy_frame, width=10)
        self.entry_qty.grid(row=0, column=3)

        tk.Button(buy_frame, text="Добавить в корзину", command=self.add_to_cart).grid(row=0, column=4, padx=5)
        tk.Button(self.root, text='Показать корзину', command=self.show_cart).pack(pady=5)
        tk.Button(self.root, text="ОФОРМИТЬ ЧЕК", command=self.finalize_purchase).pack(pady=10)

    def add_to_cart(self):
        p_id = self.entry_id.get()
        qty = self.entry_qty.get()

        if not p_id or not qty:
            messagebox.showwarning("Ошибка", "Заполните все поля")
            return
        else:
            self.cart.append((int(p_id), int(qty)))
            messagebox.showinfo("Корзина", f"Товар {p_id} добавлен. Всего позиций: {len(self.cart)}")
            self.entry_id.delete(0, tk.END)
            self.entry_qty.delete(0, tk.END)
            self.load_data()

    def finalize_purchase(self):
        if not self.cart:
            messagebox.showwarning("Ошибка", "Корзина пуста!")
            return
        success, result = self.shop.make_purchase(1, self.cart)
        if success:
            str_cart = self.get_cart_list()
            messagebox.showinfo("Успех", f"Чек №{result} оформлен ({len(self.cart)}шт)\n{str_cart}")
            self.cart = []
            self.load_data()
        else:
            messagebox.showerror("Ошибка", f"Проблема при оформлении: {result}")

    def get_cart_list(self):
        str_cart = ''
        for p_id, qty in self.cart:
            str_cart += f'Товар id({p_id}) - {qty} шт.\n'
        return str_cart

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for product in self.shop.get_all_products():
            self.tree.insert("", tk.END, values=product)

    def show_cart(self):
        if not self.cart:
            messagebox.showinfo("Корзина", "Ваша корзина пока пуста.")
            return
        str_cart = self.get_cart_list()
        messagebox.showinfo('Ваша корзина', str_cart)

if __name__ == '__main__':
    root = tk.Tk()
    app = StoreApp(root)
    app.load_data()
    root.mainloop()







