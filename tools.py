import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os

# ---------------- Database Setup ----------------
db_path = os.path.join('tools_shop.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        price REAL NOT NULL
    )
''')

conn.commit()

GST_RATE = 0.18  # GST rate (18%)


# ---------------- Tkinter Setup ----------------
window = tk.Tk()
window.title("Tool Shop - Product Management (Scrollable)")
window.geometry("700x600")

# Scrollable Frame Setup
main_frame = tk.Frame(window)
main_frame.pack(fill=tk.BOTH, expand=1)

canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

second_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=second_frame, anchor="nw")

# ---------------- Functions ----------------
def add_product():
    name = name_entry.get()
    category = category_entry.get()
    price = price_entry.get()

    if name and price:
        try:
            price = float(price)
            cursor.execute('INSERT INTO products (name, category, price) VALUES (?, ?, ?)', (name, category, price))
            conn.commit()
            messagebox.showinfo("Success", f"Product '{name}' added successfully!")
            name_entry.delete(0, tk.END)
            category_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number.")
    else:
        messagebox.showwarning("Input Error", "Please fill at least Name and Price.")


def show_products():
    cursor.execute('SELECT * FROM products')
    records = cursor.fetchall()
    display_area.delete(1.0, tk.END)

    if records:
        for record in records:
            product_id, name, category, price = record
            price_with_gst = price + (price * GST_RATE)
            display_area.insert(tk.END, f"ID: {product_id}, Name: {name}, Category: {category}, Price: {price:.2f}, Price with GST: {price_with_gst:.2f}\n")
    else:
        display_area.insert(tk.END, "No products found.\n")


def search_product():
    search_name = search_entry.get()

    if search_name:
        cursor.execute('SELECT * FROM products WHERE name = ?', (search_name,))
        record = cursor.fetchone()
        display_area.delete(1.0, tk.END)

        if record:
            product_id, name, category, price = record
            price_with_gst = price + (price * GST_RATE)
            display_area.insert(tk.END, f"ID: {product_id}\nName: {name}\nCategory: {category}\nPrice: {price:.2f}\nPrice with GST: {price_with_gst:.2f}")
        else:
            display_area.insert(tk.END, "Product not found.\n")
    else:
        messagebox.showwarning("Input Error", "Please enter a product name to search.")


def update_product():
    product_id = update_id_entry.get()
    new_name = update_name_entry.get()
    new_category = update_category_entry.get()
    new_price = update_price_entry.get()

    if product_id and new_name and new_price:
        try:
            new_price = float(new_price)
            cursor.execute('''
                UPDATE products
                SET name = ?, category = ?, price = ?
                WHERE id = ?
            ''', (new_name, new_category, new_price, product_id))
            conn.commit()
            messagebox.showinfo("Success", f"Product ID {product_id} updated successfully!")
            update_id_entry.delete(0, tk.END)
            update_name_entry.delete(0, tk.END)
            update_category_entry.delete(0, tk.END)
            update_price_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number.")
    else:
        messagebox.showwarning("Input Error", "Please fill all fields to update.")


def delete_product():
    product_id = delete_id_entry.get()

    if product_id:
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        record = cursor.fetchone()

        if record:
            cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
            conn.commit()
            messagebox.showinfo("Success", f"Product ID {product_id} deleted successfully!")
            delete_id_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Product ID not found.")
    else:
        messagebox.showwarning("Input Error", "Please enter Product ID to delete.")


# ---------------- UI Layout ----------------

# Title
tk.Label(second_frame, text="Tool Shop Management", font=("Arial", 20, "bold")).pack(pady=10)

# Add Product Section
tk.Label(second_frame, text="Product Name:").pack()
name_entry = tk.Entry(second_frame, width=30)
name_entry.pack(pady=5)

tk.Label(second_frame, text="Category:").pack()
category_entry = tk.Entry(second_frame, width=30)
category_entry.pack(pady=5)

tk.Label(second_frame, text="Price (without GST):").pack()
price_entry = tk.Entry(second_frame, width=30)
price_entry.pack(pady=5)

tk.Button(second_frame, text="Add Product", bg="lightgreen", width=20, command=add_product).pack(pady=10)

# Show All Products Button
tk.Button(second_frame, text="Show All Products", bg="lightblue", width=20, command=show_products).pack(pady=10)

# Display Area
display_area = tk.Text(second_frame, height=15, width=70)
display_area.pack(pady=20)

# Search Section
tk.Label(second_frame, text="Search Product by Name:").pack()
search_entry = tk.Entry(second_frame, width=30)
search_entry.pack(pady=5)

tk.Button(second_frame, text="Search Product", bg="lightyellow", width=20, command=search_product).pack(pady=10)

# Update Section
tk.Label(second_frame, text="Update Product Details").pack(pady=10)

tk.Label(second_frame, text="Product ID to Update:").pack()
update_id_entry = tk.Entry(second_frame, width=30)
update_id_entry.pack(pady=5)

tk.Label(second_frame, text="New Name:").pack()
update_name_entry = tk.Entry(second_frame, width=30)
update_name_entry.pack(pady=5)

tk.Label(second_frame, text="New Category:").pack()
update_category_entry = tk.Entry(second_frame, width=30)
update_category_entry.pack(pady=5)

tk.Label(second_frame, text="New Price:").pack()
update_price_entry = tk.Entry(second_frame, width=30)
update_price_entry.pack(pady=5)

tk.Button(second_frame, text="Update Product", bg="orange", width=20, command=update_product).pack(pady=10)

# Delete Section
tk.Label(second_frame, text="Delete Product").pack(pady=10)

tk.Label(second_frame, text="Product ID to Delete:").pack()
delete_id_entry = tk.Entry(second_frame, width=30)
delete_id_entry.pack(pady=5)

tk.Button(second_frame, text="Delete Product", bg="red", fg="white", width=20, command=delete_product).pack(pady=10)

# Safe Window Close
def on_closing():
    conn.close()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

# Run App
window.mainloop()
