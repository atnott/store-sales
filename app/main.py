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

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for product in self.shop.get_all_products():
            self.tree.insert("", tk.END, values=product)







if __name__ == '__main__':
    root = tk.Tk()
    app = StoreApp(root)
    root.mainloop()







