import sqlite3

DB_NAME = 'stickers.db'

# Initialize stickers table
def init_stickers_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stickers (
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

# Seed sticker products if empty
def seed_stickers():
    sticker_products = [
        # ADD A STOCK VALUE (e.g., 10) TO EACH PRODUCT HERE
        # Format: (name, price, image_url, alt, stock)
        ("DBTK HOLOGRAPHIC STICKER PACK",
         "₱300",
         "https://dbtkco.com/cdn/shop/products/2_2_1.jpg?v=1677252535",
         "stashKeychain", 10),
        ("DBTK Cipher Logo",
         "₱80",
         "https://dbtkco.com/cdn/shop/products/ciphersmalldecal.jpg?v=1648003065",
         "stashKeychainGreen", 25),
        ("SNEAKY KID LOGO CAR STICKER",
         "₱150",
         "https://dbtkco.com/cdn/shop/products/sneakydecal.jpg?v=1648002827",
         "stashKeychainRed", 15),
        ("OG DBTK Logo", # Corrected typo: removed extra closing quote
         "₱100",
         "https://dbtkco.com/cdn/shop/products/images.jpg?v=1572079706",
         "buckleBelt", 30),
    ]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM stickers")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            # UPDATED INSERT STATEMENT to include 'stock'
            "INSERT INTO stickers (name, price, image_url, alt, stock) VALUES (?, ?, ?, ?, ?)",
            sticker_products
        )
        conn.commit()

    conn.close()

# Fetch all sticker products
def get_all_stickers():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Ensure 'stock' is selected
    cursor.execute("SELECT id, name, price, image_url, alt, stock FROM stickers")
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
    init_stickers_db()
    seed_stickers()
    products = get_all_stickers()
    for product in products:
        print(product)