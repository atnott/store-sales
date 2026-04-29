import tkinter as tk
from tkinter import ttk, messagebox
from models import Shop

class StoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Shop Manager')
        self.root.geometry("600x500")

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

        tk.Button(self.root, text="Обновить склад", command=self.load_data).pack(pady=5)

        buy_frame = tk.LabelFrame(self.root, text="Оформить покупку")
        buy_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(buy_frame, text="ID товара:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = tk.Entry(buy_frame, width=10)
        self.entry_id.grid(row=0, column=1)

        tk.Label(buy_frame, text="Количество товара:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_qty = tk.Entry(buy_frame, width=10)
        self.entry_qty.grid(row=0, column=3)

        tk.Button(buy_frame, text="Купить", bg="white", fg="black", command=self.buy_action).grid(row=0, column=4, padx=10)

    def buy_action(self):
        p_id = self.entry_id.get()
        qty = self.entry_qty.get()

        if not p_id or not qty:
            messagebox.showwarning("Ошибка", "Заполните все поля")
            return

        success, result = self.shop.make_purchase(1, [(int(p_id), int(qty))])

        if success:
            messagebox.showinfo("Успех", f"Покупка совершена! Чек №{result}")
            self.load_data()  # Сразу обновляем остатки в таблице
        else:
            messagebox.showerror("Ошибка склада", f"Не удалось: {result}")

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for product in self.shop.get_all_products():
            self.tree.insert("", tk.END, values=product)


if __name__ == '__main__':
    root = tk.Tk()
    app = StoreApp(root)
    root.mainloop()







