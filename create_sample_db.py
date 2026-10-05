"""
Create a sample e-commerce SQLite database for testing the QueryMind application.
Run this script to generate 'sample_ecommerce.db' with customers, products, orders, etc.
"""

import sqlite3
import os
import random
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "sample_ecommerce.db")


def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # --- Create tables ---
    cursor.executescript("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            city TEXT NOT NULL,
            phone TEXT,
            registration_date DATE NOT NULL,
            status TEXT DEFAULT 'active'
        );

        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        );

        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            price REAL NOT NULL,
            stock_quantity INTEGER DEFAULT 0,
            created_date DATE NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );

        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );

        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
    """)

    # --- Seed data ---
    cities = ["Mumbai", "Delhi", "Bangalore", "Pune", "Chennai", "Hyderabad", "Kolkata", "Jaipur", "Ahmedabad", "Lucknow"]
    first_names = ["Rahul", "Priya", "Amit", "Sneha", "Vikram", "Anita", "Rohit", "Kavita", "Suresh", "Meena",
                   "Arun", "Divya", "Sanjay", "Pooja", "Rajesh", "Neha", "Manish", "Swati", "Deepak", "Ritu",
                   "Ajay", "Sunita", "Kiran", "Lakshmi", "Nitin"]
    last_names = ["Sharma", "Patel", "Singh", "Kumar", "Gupta", "Mehta", "Joshi", "Verma", "Reddy", "Nair",
                  "Iyer", "Das", "Mishra", "Rao", "Pillai"]
    statuses = ["active", "active", "active", "active", "inactive"]

    # Insert customers
    random.seed(42)
    customers = []
    for i in range(50):
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        name = f"{fname} {lname}"
        email = f"{fname.lower()}.{lname.lower()}{i}@{'gmail.com' if random.random() > 0.3 else 'yahoo.com'}"
        city = random.choice(cities)
        phone = f"+91 {random.randint(70000, 99999)} {random.randint(10000, 99999)}"
        reg_date = (datetime.now() - timedelta(days=random.randint(1, 730))).strftime("%Y-%m-%d")
        status = random.choice(statuses)
        customers.append((name, email, city, phone, reg_date, status))

    cursor.executemany(
        "INSERT INTO customers (name, email, city, phone, registration_date, status) VALUES (?, ?, ?, ?, ?, ?)",
        customers,
    )

    # Insert categories
    categories = [
        ("Electronics", "Phones, laptops, tablets, and accessories"),
        ("Clothing", "Men's and women's fashion"),
        ("Home & Kitchen", "Furniture, appliances, and kitchen items"),
        ("Books", "Fiction, non-fiction, and academic books"),
        ("Sports", "Sports equipment and fitness gear"),
        ("Beauty", "Skincare, makeup, and personal care"),
    ]
    cursor.executemany("INSERT INTO categories (name, description) VALUES (?, ?)", categories)

    # Insert products
    product_data = [
        # Electronics
        ("iPhone 15", 1, 79999, 45), ("Samsung Galaxy S24", 1, 69999, 60),
        ("MacBook Air M3", 1, 129999, 20), ("Dell XPS 15", 1, 109999, 25),
        ("iPad Pro", 1, 89999, 35), ("Sony WH-1000XM5", 1, 24999, 100),
        ("AirPods Pro", 1, 24900, 150), ("Lenovo ThinkPad", 1, 85000, 30),
        # Clothing
        ("Men's Formal Shirt", 2, 1499, 200), ("Women's Kurti", 2, 999, 300),
        ("Denim Jeans", 2, 1999, 180), ("Cotton Saree", 2, 2499, 120),
        ("Sports T-Shirt", 2, 799, 250), ("Winter Jacket", 2, 3499, 80),
        # Home & Kitchen
        ("Pressure Cooker", 3, 2599, 90), ("Non-Stick Pan Set", 3, 1899, 110),
        ("LED Desk Lamp", 3, 1299, 150), ("Coffee Maker", 3, 4999, 40),
        ("Air Purifier", 3, 12999, 25), ("Water Purifier", 3, 15999, 30),
        # Books
        ("The Alchemist", 4, 299, 500), ("Atomic Habits", 4, 499, 400),
        ("Sapiens", 4, 599, 350), ("Rich Dad Poor Dad", 4, 399, 450),
        # Sports
        ("Yoga Mat", 5, 999, 200), ("Cricket Bat", 5, 2999, 70),
        ("Running Shoes", 5, 3999, 120), ("Fitness Band", 5, 1999, 180),
        # Beauty
        ("Face Moisturizer", 6, 599, 300), ("Sunscreen SPF 50", 6, 499, 350),
        ("Hair Oil", 6, 349, 400), ("Lip Balm Set", 6, 249, 500),
    ]
    products = []
    for name, cat_id, price, stock in product_data:
        created = (datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d")
        products.append((name, cat_id, price, stock, created))

    cursor.executemany(
        "INSERT INTO products (name, category_id, price, stock_quantity, created_date) VALUES (?, ?, ?, ?, ?)",
        products,
    )

    # Insert orders
    order_statuses = ["completed", "completed", "completed", "pending", "shipped", "cancelled"]
    orders = []
    for i in range(120):
        customer_id = random.randint(1, 50)
        order_date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
        status = random.choice(order_statuses)
        total = 0  # will be updated
        orders.append((customer_id, order_date, total, status))

    cursor.executemany(
        "INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES (?, ?, ?, ?)",
        orders,
    )

    # Insert order items and update totals
    for order_id in range(1, 121):
        num_items = random.randint(1, 4)
        total = 0
        for _ in range(num_items):
            product_id = random.randint(1, len(product_data))
            quantity = random.randint(1, 3)
            unit_price = product_data[product_id - 1][2]
            total += unit_price * quantity
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                (order_id, product_id, quantity, unit_price),
            )
        cursor.execute("UPDATE orders SET total_amount = ? WHERE id = ?", (total, order_id))

    conn.commit()
    conn.close()
    print(f"[OK] Sample database created at: {DB_PATH}")
    print(f"   - 50 customers")
    print(f"   - 6 categories")
    print(f"   - {len(product_data)} products")
    print(f"   - 120 orders")
    print(f"\n   Use this path to connect in QueryMind:")
    print(f"   {os.path.abspath(DB_PATH)}")


if __name__ == "__main__":
    create_database()
