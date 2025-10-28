import sqlite3

DB_NAME = 'tom.db' # Changed to 'tom.db' for consistency

# Initialize tom table
def init_tom_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tom (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            image_url TEXT,
            alt TEXT,
            stock INTEGER DEFAULT 0 -- Added stock column
        )
    ''')
    conn.commit()
    conn.close()

# Seed tom products if empty
def seed_tom():
    tom_products = [
        # Added a default stock value (e.g., 10) to each product
        ("TOM CLUTCH HEAD BUST", "₱950", "https://dbtkco.com/cdn/shop/files/DB100345_3d15d194-af8f-4555-ad6f-0cc0688e7136.jpg?v=1745565699", "Cotton Toms", 12),
        ("TOM CLUTCH PLUSHIE", "₱1600", "https://dbtkco.com/cdn/shop/files/DB100317_814d8473-02e5-42f3-b48f-115fb62a1316.jpg?v=1745566050", "Cotton Toms", 8),
    ]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM tom")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO tom (name, price, image_url, alt, stock) VALUES (?, ?, ?, ?, ?)", # Added stock column
            tom_products
        )
        conn.commit()

    conn.close()

# Fetch all tom products
def get_all_tom():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, image_url, alt, stock FROM tom") # Select the new 'stock' column
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row["id"],
            "name": row["name"],
            "price": row["price"],
            "image": row["image_url"],
            "alt": row["alt"],
            "stock": row["stock"] # Include 'stock' in the returned dictionary
        }
        for row in rows
    ]

# Initialize and seed when run directly
if __name__ == "__main__":
    init_tom_db()
    seed_tom()
    products = get_all_tom()
    for product in products:
        print(product)