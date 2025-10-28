import sqlite3

DB_NAME = 'tshirt.db'

# Initialize tshirt table
def init_tshirt_db():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tshirt (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            image_url TEXT,
            alt TEXT,
            stock INTEGER DEFAULT 0  -- Add this line for the stock column
        );
    ''')
    con.commit()
    con.close()

# Seed tshirt products if table is empty
def seed_tshirt():
    tshirt_products = [
        ("DAILY TEE - BLACK", "₱950", "https://dbtkco.com/cdn/shop/files/Daily_Black_4feb3eb7-463d-4045-b79e-da99c8d596b1.jpg?v=1746163536", "dailyTee", 10), # Added a default stock value (e.g., 10)
        ("MICRO MERGE TEE", "₱1000", "https://dbtkco.com/cdn/shop/files/MICRO_MERGE_1.png?v=1734767697", "microMerge", 15),
        ("OG BLACK ELEMENTARY - DARK EDEN GREEN", "₱900", "https://dbtkco.com/cdn/shop/files/OGELEMENTARY5.png?v=1734767308", "ogBlack", 8),
        ("KIDS IN PROGRESS BOWLING SHIRT", "₱1100", "https://dbtkco.com/cdn/shop/files/IMG-2423.jpg?v=1743779781", "kidsBowling", 12),
        ("D-PARKED PANELED JACKET", "₱1000", "https://dbtkco.com/cdn/shop/files/D-SPARKPANELEDJACKET5.jpg?v=1728696742", "dParked", 7),
        ("OAKSHADE WORKWEAR", "₱1000", "https://dbtkco.com/cdn/shop/files/OAKSHADEWORKWEARJACKET1.jpg?v=1737095917", "oakShade", 20),
        ("90'S ODYSSEY POLO", "₱900", "https://dbtkco.com/cdn/shop/files/90_SODYSSEY1.jpg?v=1736499817", "odyssey", 5),
        ("ATLAS TEE", "₱1000", "https://dbtkco.com/cdn/shop/files/atlas_black_7580234c-d283-45f2-821c-a0278572cf84.png?v=1738661449", "atlasTee", 10),
        ("SPEED CLUB TEE - CREAM", "₱1000", "https://dbtkco.com/cdn/shop/files/SPEEDCLUB3.jpg?v=1732589423", "atlasTee", 9),
        ("HYPERDRIVE TEE - BLACK", "₱950", "https://dbtkco.com/cdn/shop/files/HYPERDRIVE1.jpg?v=1732587875", "atlasTee", 11),
        ("CHASER SPLICE TEE - BLACK & GRAY", "₱1650", "https://dbtkco.com/cdn/shop/files/CHASERSPLICE1.jpg?v=1726117991", "atlasTee", 6),
        ("CIPHER TEE 2025 - ORANGE", "₱1000", "https://dbtkco.com/cdn/shop/files/CIPHER-ORANGE-WEB.jpg?v=1743406716", "atlasTee", 14),
    ]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if table has data
    cursor.execute("SELECT COUNT(*) FROM tshirt")
    if cursor.fetchone()[0] == 0:
        # Modified the INSERT statement to include the stock column
        cursor.executemany(
            "INSERT INTO tshirt (name, price, image_url, alt, stock) VALUES (?, ?, ?, ?, ?)",
            tshirt_products
        )
        conn.commit()

    conn.close()

# Fetch all tshirt products
def get_all_tshirt():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    # FIX: Include the id column in the SELECT statement
    cur.execute("SELECT id, name, price, image_url, alt, stock FROM tshirt")
    rows = cur.fetchall()
    con.close()
    # FIX: Include 'id' in the returned dictionary
    return [{"id": row[0], "name": row[1], "price": row[2], "image": row[3], "alt": row[4], "stock": row[5]} for row in rows]

# Run initialization and seeding when executed directly
if __name__ == "__main__":
    init_tshirt_db()
    seed_tshirt()
    products = get_all_tshirt()
    for product in products:
        print(product)