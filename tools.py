import sqlite3
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

# Database setup
conn = sqlite3.connect('tools_shop.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER DEFAULT 0
    )
''')
conn.commit()

class AddProductPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="Add Product", font=("Segoe UI", 18, "bold")).pack(pady=20)

        self.name_entry = self.create_entry("Product Name:")
        self.category_entry = self.create_entry("Category:")
        self.price_entry = self.create_entry("Price:")
        self.quantity_entry = self.create_entry("Quantity:")

        ttk.Button(self, text="Add", bootstyle=SUCCESS, command=self.add_product).pack(pady=10)
        ttk.Button(self, text="Back", bootstyle=SECONDARY, command=lambda: controller.show_frame(HomePage)).pack(pady=10)

    def create_entry(self, label_text):
        frame = ttk.LabelFrame(self, text=label_text, padding=10)
        frame.pack(pady=5, fill='x')
        entry = ttk.Entry(frame, width=40)
        entry.pack(padx=5, pady=5)
        return entry

    def add_product(self):
        name = self.name_entry.get()
        category = self.category_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        if not name or not category or not price or not quantity:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showwarning("Input Error", "Price and Quantity must be numbers!")
            return

        cursor.execute('INSERT INTO products (name, category, price, quantity) VALUES (?, ?, ?, ?)', (name, category, price, quantity))
        conn.commit()
        messagebox.showinfo("Success", "Product added successfully!")

class BillingPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="Billing", font=("Segoe UI", 18, "bold")).pack(pady=20)

        self.cart = []
        self.total_amount = 0

        self.name_entry = self.create_entry("Product Name:")
        self.quantity_entry = self.create_entry("Quantity:")

        ttk.Button(self, text="Add to Cart", bootstyle=SUCCESS, command=self.add_to_cart).pack(pady=10)

        self.cart_display = ttk.Treeview(self, columns=("Product", "Quantity", "Total"), show='headings', bootstyle=INFO)
        for col in ["Product", "Quantity", "Total"]:
            self.cart_display.heading(col, text=col)
        self.cart_display.pack(expand=True, fill='both', padx=10, pady=10)

        self.total_label = ttk.Label(self, text="Total: 0", font=("Segoe UI", 12, "bold"))
        self.total_label.pack(pady=10)

        ttk.Button(self, text="Back", bootstyle=SECONDARY, command=lambda: controller.show_frame(HomePage)).pack(pady=10)

    def create_entry(self, label_text):
        frame = ttk.LabelFrame(self, text=label_text, padding=10)
        frame.pack(pady=5, fill='x')
        entry = ttk.Entry(frame, width=40)
        entry.pack(padx=5, pady=5)
        return entry

    def add_to_cart(self):
        product_name = self.name_entry.get()
        quantity_sold = self.quantity_entry.get()

        if not product_name or not quantity_sold:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        try:
            quantity_sold = int(quantity_sold)
        except ValueError:
            messagebox.showwarning("Input Error", "Quantity must be a number!")
            return

        cursor.execute('SELECT id, quantity, price FROM products WHERE name = ?', (product_name,))
        result = cursor.fetchone()

        if result:
            prod_id, current_stock, price = result
            if quantity_sold <= current_stock:
                cursor.execute('UPDATE products SET quantity=? WHERE id=?', (current_stock - quantity_sold, prod_id))
                conn.commit()
                total = price * quantity_sold
                self.cart.append((product_name, quantity_sold, total))
                self.total_amount += total
                self.cart_display.insert("", "end", values=(product_name, quantity_sold, total))
                self.total_label.config(text=f"Total: {self.total_amount}")
            else:
                messagebox.showwarning("Stock Error", "Not enough stock!")
        else:
            messagebox.showwarning("Not Found", "Product not found!")

class AdjustStockPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="Adjust Stock", font=("Segoe UI", 18, "bold")).pack(pady=20)

        self.name_entry = self.create_entry("Product Name:")
        self.quantity_entry = self.create_entry("New Quantity:")

        ttk.Button(self, text="Update Stock", bootstyle=SUCCESS, command=self.update_stock).pack(pady=10)
        ttk.Button(self, text="Back", bootstyle=SECONDARY, command=lambda: controller.show_frame(HomePage)).pack(pady=10)

    def create_entry(self, label_text):
        frame = ttk.LabelFrame(self, text=label_text, padding=10)
        frame.pack(pady=5, fill='x')
        entry = ttk.Entry(frame, width=40)
        entry.pack(padx=5, pady=5)
        return entry

    def update_stock(self):
        product_name = self.name_entry.get()
        new_quantity = self.quantity_entry.get()

        if not product_name or not new_quantity:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        try:
            new_quantity = int(new_quantity)
        except ValueError:
            messagebox.showwarning("Input Error", "Quantity must be a number!")
            return

        cursor.execute('SELECT id FROM products WHERE name = ?', (product_name,))
        result = cursor.fetchone()

        if result:
            cursor.execute('UPDATE products SET quantity=? WHERE id=?', (new_quantity, result[0]))
            conn.commit()
            messagebox.showinfo("Success", "Stock updated successfully!")
        else:
            messagebox.showwarning("Not Found", "Product not found!")

class DeleteProductPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="Delete Product", font=("Segoe UI", 18, "bold")).pack(pady=20)

        self.name_entry = self.create_entry("Product Name:")

        ttk.Button(self, text="Delete", bootstyle=DANGER, command=self.delete_product).pack(pady=10)
        ttk.Button(self, text="Back", bootstyle=SECONDARY, command=lambda: controller.show_frame(HomePage)).pack(pady=10)

    def create_entry(self, label_text):
        frame = ttk.LabelFrame(self, text=label_text, padding=10)
        frame.pack(pady=5, fill='x')
        entry = ttk.Entry(frame, width=40)
        entry.pack(padx=5, pady=5)
        return entry

    def delete_product(self):
        product_name = self.name_entry.get()
        cursor.execute('SELECT id FROM products WHERE name=?', (product_name,))
        if cursor.fetchone():
            cursor.execute('DELETE FROM products WHERE name=?', (product_name,))
            conn.commit()
            messagebox.showinfo("Success", f"Product '{product_name}' deleted successfully!")
        else:
            messagebox.showwarning("Not Found", "Product not found!")

class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="View Products", font=("Segoe UI", 18, "bold")).pack(pady=20)

        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Category", "Price", "Quantity"), show='headings', bootstyle=INFO, height=12)
        for col in ["ID", "Name", "Category", "Price", "Quantity"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(padx=10, pady=10)

        ttk.Button(self, text="Load Products", bootstyle=PRIMARY, command=self.load_products).pack(pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(anchor='se', pady=10)
        buttons = [
            ("Add Product", AddProductPage),
            ("Billing", BillingPage),
            ("Adjust Stock", AdjustStockPage),
            ("Delete Product", DeleteProductPage),
        ]
        for i, (text, page) in enumerate(buttons):
            ttk.Button(btn_frame, text=text, bootstyle=SECONDARY, width=18, command=lambda p=page: controller.show_frame(p)).grid(row=0, column=i, padx=5)

    def load_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        cursor.execute('SELECT * FROM products')
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

class ProductManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        style = ttk.Style("superhero")
        self.title("Product Manager")
        self.geometry("900x700")
        self.configure(bg="#726f6f")

        self.frames = {}
        container = ttk.Frame(self, padding=20, borderwidth=3, relief="ridge")
        container.pack(expand=True, fill='both')

        for F in (HomePage, AddProductPage, BillingPage, AdjustStockPage, DeleteProductPage):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(HomePage)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()

if __name__ == "__main__":
    app = ProductManagerApp()
    app.mainloop()
    conn.close()
