import sqlite3

DB_NAME = "footwear.db"

# --- Initialize Footwear Table ---
def init_footwear_db():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS footwear (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            image_url TEXT,
            alt TEXT,
            stock INTEGER DEFAULT 0
        );
    ''')
    con.commit()
    con.close()

# --- Seed Sample Footwear Data ---
def seed_footwear():
    products = [
        # Added a default stock value (e.g., 10) to each product
        ("BURROW CAMO CIPHER SLIDES - BROWN/PINK/PEACH", "₱700", "https://dbtkco.com/cdn/shop/files/SLIDES_2.jpg?v=1722582608", "Black Sneakers", 10)
    ]

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    # Only seed if table is empty
    cur.execute("SELECT COUNT(*) FROM footwear")
    if cur.fetchone()[0] == 0:
        cur.executemany('''
            INSERT INTO footwear (name, price, image_url, alt, stock) VALUES (?, ?, ?, ?, ?)
        ''', products)
        con.commit()

    con.close()

# --- Fetch All Footwear ---
def get_all_footwear():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT id, name, price, image_url, alt, stock FROM footwear")
    rows = cur.fetchall()
    con.close()
    return [{
            "id": row["id"],
            "name": row["name"],
            "price": row["price"],
            "image": row["image_url"],
            "alt": row["alt"],
            "stock": row["stock"]
        }
        for row in rows
        ]

# Run initialization and seeding when executed directly
if __name__ == "__main__":
    init_footwear_db()
    seed_footwear()
    products = get_all_footwear()
    for product in products:
        print(product)