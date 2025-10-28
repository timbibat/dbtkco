import sqlite3

DB_NAME = 'accessories.db'

# Initialize accessories table
def init_accessories_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accessories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            image_url TEXT,
            alt TEXT,
            stock INTEGER DEFAULT 0  -- ADDED: Stock column with a default
        )
    ''')
    conn.commit()
    conn.close()

# Seed accessories products if table is empty
def seed_accessories():
    accessories_products = [
        # ADD A STOCK VALUE (e.g., 10) TO EACH PRODUCT HERE
        # Format: (name, price, image_url, alt, stock)
        ("MONROE SILK SCARF", "₱850", "https://dbtkco.com/cdn/shop/files/DB100596.jpg?v=1747904337", "stashKeychain", 10),
        ("VEGAS SILK SCARF", "₱850", "https://dbtkco.com/cdn/shop/files/DB100588_23083015-2f6a-4442-8d42-826d71b2c3f0.jpg?v=1747981011", "stashKeychainGreen", 8),
        ("SPARK D LEATHER CARD HOLDER - BLACK", "₱1100", "https://dbtkco.com/cdn/shop/files/FA445A82-AEEB-4DB0-AE0B-643FF37E76D7.jpg?v=1748256694", "cardHolder", 15),
        ("SPARK D LEATHER CARD HOLDER - GREEN", 
         "₱1100", 
         "https://dbtkco.com/cdn/shop/files/08B030DD-374D-4C70-AE37-26BE64829A2D.jpg?v=1748256628", 
         "buckleBelt", 12),
        ("DBTK x Bicycle Playing Cards", "₱799", "https://dbtkco.com/cdn/shop/files/03_Carousel_Post_2.jpg?v=1745484924", "fan", 0), # Example: out of stock
        ("WOODLAND CIPHER UMBRELLA", "₱900", "https://dbtkco.com/cdn/shop/files/WOODLANDCIPHERUMBRELLA1.jpg?v=1721958145", "umbrella", 7),
        ("DBTK SLANT KEYCHAIN", "₱150", "https://dbtkco.com/cdn/shop/products/Artboard1copy4.png?v=1676946380", "umbrella", 2),
        # Add more products with their stock values
    ]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if table has data
    cursor.execute("SELECT COUNT(*) FROM accessories")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            # UPDATED INSERT STATEMENT to include 'stock'
            "INSERT INTO accessories (name, price, image_url, alt, stock) VALUES (?, ?, ?, ?, ?)",
            accessories_products
        )
        conn.commit()

    conn.close()

# Fetch all accessories products
def get_all_accessories():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Ensure 'stock' is selected
    cursor.execute("SELECT id, name, price, image_url, alt, stock FROM accessories")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row["id"],
            "name": row["name"],
            "price": row["price"],
            "image": row["image_url"],
            "alt": row["alt"],
            "stock": row["stock"] # Include stock in the returned dict
        }
        for row in rows
    ]