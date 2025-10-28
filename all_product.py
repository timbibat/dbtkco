import sqlite3

DB_NAME = 'all_product.db'

# Initialize DB and create table
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            image_url TEXT NOT NULL,
            alt TEXT
        )
    ''')
    conn.commit()
    conn.close()

def seed_products():
    products = [
        (1, 
         "DAILY TEE - BLACK", 
         "₱950", 
         "https://dbtkco.com/cdn/shop/files/Daily_Black_4feb3eb7-463d-4045-b79e-da99c8d596b1.jpg?v=1746163536", 
         "dailyTee"),
        (2, 
         "MICRO MERGE TEE", 
         "₱1000", 
         "https://dbtkco.com/cdn/shop/files/MICRO_MERGE_1.png?v=1734767697", 
         "microMerge"),
        (3, 
         "OG BLACK ELEMENTARY - DARK EDEN GREEN", 
         "₱900", 
         "https://dbtkco.com/cdn/shop/files/OGELEMENTARY5.png?v=1734767308", 
         "ogBlack"),
        (4, 
         "KIDS IN PROGRESS BOWLING SHIRT", 
         "₱1100", 
         "https://dbtkco.com/cdn/shop/files/IMG-2423.jpg?v=1743779781", 
         "kidsBowling"),
        (5, 
         "D-PARKED PANELED JACKET", 
         "₱1000", 
         "https://dbtkco.com/cdn/shop/files/D-SPARKPANELEDJACKET5.jpg?v=1728696742", 
         "dParked"),
        (6, 
         "OAKSHADE WORKWEAR", 
         "₱1000", 
         "https://dbtkco.com/cdn/shop/files/OAKSHADEWORKWEARJACKET1.jpg?v=1737095917", 
         "oakShade"),
        (7, 
         "90'S ODYSSEY POLO", 
         "₱900", 
         "https://dbtkco.com/cdn/shop/files/90_SODYSSEY1.jpg?v=1736499817", 
         "odyssey"),
        (8, 
         "ATLAS TEE", 
         "₱1000", 
         "https://dbtkco.com/cdn/shop/files/atlas_black_7580234c-d283-45f2-821c-a0278572cf84.png?v=1738661449", 
         "atlasTee"),
        (9, 
         "SPEED CLUB TEE - CREAM", 
         "₱1000", 
         "https://dbtkco.com/cdn/shop/files/SPEEDCLUB3.jpg?v=1732589423", 
         "atlasTee"),
        (10, 
         "HYPERDRIVE TEE - BLACK", 
         "₱950", 
         "https://dbtkco.com/cdn/shop/files/HYPERDRIVE1.jpg?v=1732587875", 
         "atlasTee"),
        (11, 
         "CHASER SPLICE TEE - BLACK & GRAY", 
         "₱1650", 
         "https://dbtkco.com/cdn/shop/files/CHASERSPLICE1.jpg?v=1726117991", 
         "atlasTee"),
        (12, 
         "CIPHER TEE 2025 - ORANGE", 
         "₱1000", 
         "https://dbtkco.com/cdn/shop/files/CIPHER-ORANGE-WEB.jpg?v=1743406716", 
         "atlasTee"),
        (13, "BURROW CAMO CIPHER SLIDES - BROWN/PINK/PEACH", "₱700", "https://dbtkco.com/cdn/shop/files/SLIDES_2.jpg?v=1722582608", "Black Sneakers"),
        (14, "TOON CLUTCH CORDORUY DAD HAT", "₱1200", "https://dbtkco.com/cdn/shop/files/DB100329_349adc15-1a2c-43f0-bdca-6018cab1f2b0.jpg?v=1745565941", "Denim Toms"),
        (15, "TOM CLUTCH HEAD BUST CURVE SNAPBACK", "₱1200", "https://dbtkco.com/cdn/shop/files/DB100320_40548e9f-f0f5-422a-9f89-3dcf7c9fe56d.jpg?v=1745565872", "Cotton Toms"),
        (16, "TOM CLUTCH HIGH SOCKS - WHITE", "₱750", "https://dbtkco.com/cdn/shop/files/DB100234_a91bb183-a205-4ddf-8790-6bd7f7632ebb.jpg?v=1745565559", "Cotton Toms"),
        (17, "TOM CLUTCH HEAD BUST", "₱950", "https://dbtkco.com/cdn/shop/files/DB100345_3d15d194-af8f-4555-ad6f-0cc0688e7136.jpg?v=1745565699", "Cotton Toms"),
        (18, "TOM CLUTCH PLUSHIE", "₱1600", "https://dbtkco.com/cdn/shop/files/DB100317_814d8473-02e5-42f3-b48f-115fb62a1316.jpg?v=1745566050", "Cotton Toms"),
        (19, "MONROE SILK SCARF", 
         "₱850", 
         "https://dbtkco.com/cdn/shop/files/DB100596.jpg?v=1747904337", 
         "stashKeychain"),
        (20, "VEGAS SILK SCARF", 
         "₱850", 
         "https://dbtkco.com/cdn/shop/files/DB100588_23083015-2f6a-4442-8d42-826d71b2c3f0.jpg?v=1747981011", 
         "stashKeychainGreen"),
        (21, "SPARK D LEATHER CARD HOLDER - BLACK", 
         "₱1100", 
         "https://dbtkco.com/cdn/shop/files/FA445A82-AEEB-4DB0-AE0B-643FF37E76D7.jpg?v=1748256694", 
         "stashKeychainRed"),
        (22, "SPARK D LEATHER CARD HOLDER - GREEN", 
         "₱1100", 
         "https://dbtkco.com/cdn/shop/files/08B030DD-374D-4C70-AE37-26BE64829A2D.jpg?v=1748256628", 
         "buckleBelt"),
        (23, "DBTK x Bicycle Playing Cards", 
         "₱799", 
         "https://dbtkco.com/cdn/shop/files/03_Carousel_Post_2.jpg?v=1745484924", 
         "fan"),
        (24, "WOODLAND CIPHER FLASK - BLACK/GRAY", 
         "₱1100", 
         "https://dbtkco.com/cdn/shop/files/WOODLAND_CIPHER_FLASK_1.jpg?v=1721960065", 
         "toteBagCream"),
         (25, "DBTK HOLOGRAPHIC STICKER PACK", 
         "₱300", 
         "https://dbtkco.com/cdn/shop/products/2_2_1.jpg?v=1677252535", 
         "stashKeychain"),
        (26, "DBTK Cipher Logo", 
         "₱80", 
         "https://dbtkco.com/cdn/shop/products/ciphersmalldecal.jpg?v=1648003065", 
         "stashKeychainGreen"),
        (27, "SNEAKY KID LOGO CAR STICKER", 
         "₱150", 
         "https://dbtkco.com/cdn/shop/products/sneakydecal.jpg?v=1648002827", 
         "stashKeychainRed"),
        (28, "OG DBTK Logo”", 
         "₱100", 
         "https://dbtkco.com/cdn/shop/products/images.jpg?v=1572079706", 
         "buckleBelt"),
    ]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO products (id, name, price, image_url, alt) VALUES (?, ?, ?, ?, ?)", products)
        conn.commit()

    conn.close()

# Fetch all products
def get_all_products():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row["id"],
            "name": row["name"],
            "price": row["price"],
            "image": row["image_url"],  # ✅ Correct field here
            "alt": row["alt"]  # or row["name"] if no alt column
        }
        for row in rows
    ]
# Run initialization and seeding when script is executed
if __name__ == "__main__":
    init_db()
    seed_products()
    products = get_all_products()
    for product in products:
        print(product)