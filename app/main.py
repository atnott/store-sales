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

if __name__ == '__main__':
    root = tk.Tk()
    app = StoreApp(root)
    root.mainloop()







