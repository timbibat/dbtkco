from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import sqlite3
# Assuming these are all in separate files and initialized/seeded
from all_product import get_all_products, init_db, seed_products
from tom_db import get_all_tom, init_tom_db, seed_tom
from tshirt_db import get_all_tshirt, init_tshirt_db, seed_tshirt
from footwear_db import get_all_footwear, init_footwear_db, seed_footwear
from accessories_db import get_all_accessories, init_accessories_db, seed_accessories
from stickers_db import get_all_stickers, init_stickers_db, seed_stickers
import json
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Make sure this is set!

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    import re
    import sqlite3
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    # Fetch orders and calculate total earnings
    con = sqlite3.connect("orders.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM orders")
    orders = cur.fetchall()
    con.close()

    total_earnings = 0.0
    for order in orders:
        price_str = order['price']
        price_clean = float(re.sub(r'[^\d.]', '', price_str)) if price_str else 0
        qty = order['quantity'] if order['quantity'] else 1
        total_earnings += price_clean * qty

    # Fetch all Category products
    tshirt_products = get_all_tshirt()
    tom_products = get_all_tom()
    footwear_products = get_all_footwear()
    accessories_products = get_all_accessories()
    stickers_products = get_all_stickers()

    # Fetch users from users.db
    con_users = sqlite3.connect("users.db")
    con_users.row_factory = sqlite3.Row
    cur_users = con_users.cursor()
    cur_users.execute("SELECT * FROM users")
    users = cur_users.fetchall()
    con_users.close()

    return render_template(
        'admin_dashboard.html',
        orders=orders,
        total_earnings=total_earnings,
        tshirt_products=tshirt_products,
        tom_products=tom_products,
        footwear_products=footwear_products,
        accessories_products=accessories_products,
        stickers_products=stickers_products,
        users=users
    )

@app.route('/admin/clear_orders', methods=['POST'])
def clear_orders():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    import sqlite3
    con = sqlite3.connect("orders.db")
    cur = con.cursor()
    cur.execute("DELETE FROM orders")
    # Reset the auto-increment counter for the orders table
    cur.execute("DELETE FROM sqlite_sequence WHERE name='orders'")
    con.commit()
    con.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    if 'username' in session and 'cart' in session:
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        cur.execute("REPLACE INTO user_carts (username, cart) VALUES (?, ?)",
                    (session['username'], json.dumps(session['cart'])))
        con.commit()
        con.close()
    session.clear()
    return redirect(url_for('home'))

# --- Database Initialization ---
def init_orders_db():
    con = sqlite3.connect("orders.db")
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL,
            province TEXT,
            municipality TEXT,
            barangay TEXT,
            apparel TEXT NOT NULL,
            accessories TEXT NOT NULL,
            design TEXT NOT NULL,
            quantity INTEGER DEFAULT 1,
            price TEXT DEFAULT '0',
            payment_method TEXT DEFAULT 'N/A'
        );
    ''')
    con.commit()
    con.close()

def init_customers_db():
    con = sqlite3.connect("customers.db")
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        );
    ''')
    con.commit()
    con.close()

def init_products_db():
    con = sqlite3.connect("products.db")
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            image_url TEXT,
            alt TEXT
        );
    ''')
    con.commit()
    con.close()

def init_users_db():
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        );
    ''')
    con.commit()
    con.close()

def init_user_carts_db():
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_carts (
            username TEXT PRIMARY KEY,
            cart TEXT
        );
    ''')
    con.commit()
    con.close()

# --- Helper Functions (these are currently unused by the provided JS, but kept for completeness) ---
# NOTE: These functions previously connected to "products.db" which is a generic product DB.
# If products are now categorized into separate DBs (tshirt.db, tom.db, etc.),
# these helper functions would need to be updated to connect to the correct database
# based on the `source_table` parameter.
def get_product_name(product_id, source_table):
    db_name = f"{source_table.lower()}.db" # Construct DB name from source_table
    table_name = source_table.replace('_db', '') # Extract table name
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(f"SELECT name FROM {table_name} WHERE id=?", (product_id,))
    row = cur.fetchone()
    con.close()
    return row[0] if row else "Unknown"

def get_product_price(product_id, source_table):
    db_name = f"{source_table.lower()}.db"
    table_name = source_table.replace('_db', '')
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(f"SELECT price FROM {table_name} WHERE id=?", (product_id,))
    row = cur.fetchone()
    con.close()
    return row[0] if row else 0.0

def get_product_image(product_id, source_table):
    db_name = f"{source_table.lower()}.db"
    table_name = source_table.replace('_db', '')
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(f"SELECT image_url FROM {table_name} WHERE id=?", (product_id,))
    row = cur.fetchone()
    con.close()
    return row[0] if row else ""

# --- API Routes ---
from flask import session

# Add this new route to your app.py file

@app.route("/api/product_stock")
def get_product_stock():
    """API endpoint to get current stock for a specific product"""
    product_id = request.args.get('id')
    source = request.args.get('source')
    
    if not product_id or not source:
        return jsonify({"error": "Missing product ID or source"}), 400
    
    # Mapping of source names to database files and table names
    db_map = {
        'tshirt_db': ('tshirt.db', 'tshirt'),
        'tom_db': ('tom.db', 'tom'),
        'footwear_db': ('footwear.db', 'footwear'),
        'accessories_db': ('accessories.db', 'accessories'),
        'stickers_db': ('stickers.db', 'stickers'),
        'all_product': ('all_product.db', 'products'),  # Adjust if needed
    }
    
    if source not in db_map:
        return jsonify({"error": "Invalid source"}), 400
    
    db_file, table_name = db_map[source]
    
    try:
        # Handle composite ID format (e.g., 'tshirt_db-1')
        original_product_id = None
        if isinstance(product_id, str) and '-' in product_id:
            # It's a composite string ID like 'tshirt_db-1'
            original_product_id = int(product_id.split('-')[-1])
        else:
            # It's a direct integer ID
            original_product_id = int(product_id)
        
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        cur.execute(f"SELECT stock FROM {table_name} WHERE id=?", (original_product_id,))
        result = cur.fetchone()
        con.close()
        
        if result:
            return jsonify({"stock": result[0]})
        else:
            return jsonify({"error": "Product not found"}), 404
            
    except Exception as e:
        print(f"Error fetching stock for product {product_id} from {source}: {e}")
        return jsonify({"error": "Database error"}), 500

@app.route("/api/cart", methods=["GET", "POST"])
def manage_cart():
    if 'cart' not in session:
        session['cart'] = []
    
    if request.method == "GET":
        return jsonify({"items": session['cart']})
    elif request.method == "POST":
        data = request.get_json()
        
        new_cart_items = []
        for item in data.get('items', []):
            try:
                price_str = item.get('price', '0')
                cleaned_price = float(re.sub(r'[^\d.]', '', str(price_str)))
                quantity = int(item.get('quantity', 1))
                
                # Check for 'stock' key and if it's an integer
                item_stock = item.get('stock', None)
                if item_stock is not None:
                    item_stock = int(item_stock) # Convert to int

                if all(k in item for k in ['id', 'name', 'size', 'image', 'source']) and quantity > 0:
                    new_cart_items.append({
                        "id": item['id'],
                        "name": item['name'],
                        "price": cleaned_price,
                        "size": item['size'],
                        "quantity": quantity,
                        "image": item['image'],
                        "source": item['source'],
                        "stock": item_stock # Include stock in the cart item
                    })
                else:
                    print(f"Skipping malformed cart item: {item}")
            except (ValueError, TypeError) as e:
                print(f"Error processing cart item price/quantity: {item} - {e}")

        session['cart'] = new_cart_items
        session.modified = True

        if 'username' in session:
            con = sqlite3.connect("users.db")
            cur = con.cursor()
            cur.execute("REPLACE INTO user_carts (username, cart) VALUES (?, ?)",
                        (session['username'], json.dumps(session['cart'])))
            con.commit()
            con.close()
        return jsonify({"status": "saved"})

@app.route("/api/products")
def api_products():
    # Assuming all_product.py's get_all_products returns all products with a 'source' key
    # or you'll need to fetch from each category DB and combine them here.
    # For now, let's assume this returns combined data if it exists.
    return jsonify(get_all_products())

@app.route("/api/tom")
def api_tom():
    return jsonify(get_all_tom())

@app.route("/api/tshirt")
def api_tshirt():
    return jsonify(get_all_tshirt())

@app.route("/api/footwear")
def api_footwear():
    return jsonify(get_all_footwear())

@app.route("/api/accessories")
def api_accessories():
    return jsonify(get_all_accessories())

@app.route("/api/stickers")
def api_stickers():
    return jsonify(get_all_stickers())

# --- HTML Page Routes ---
@app.route("/")
def home():
    products = get_all_products()
    return render_template('home.html', products=products)

@app.route("/products")
def products():
    return jsonify(get_all_products())

@app.route("/orders")
def view_orders():
    con = sqlite3.connect("orders.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM orders")
    orders = cur.fetchall()
    con.close()
    return render_template("orders.html", orders=orders)

@app.route("/customers", methods=["GET", "POST"])
def customers():
    if request.method == "POST":
        new_customer = {
            "name": request.form["name"],
            "email": request.form["email"]
        }
        con = sqlite3.connect("customers.db")
        cur = con.cursor()
        cur.execute("INSERT INTO customers(name, email) VALUES(?, ?)", (new_customer["name"], new_customer["email"]))
        con.commit()
        con.close()
        return render_template("thank_you_customer.html", customer=new_customer)

    con = sqlite3.connect("customers.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM customers")
    customers = cur.fetchall()
    con.close()
    return render_template("customers.html", customers=customers)

@app.route("/tom_page")
def tom_page():
    tom = get_all_tom()
    return render_template("tom.html", tom=tom)

@app.route("/tshirt_page")
def tshirt_page():
    tshirts = get_all_tshirt()
    return render_template("tshirt.html", tshirts=tshirts)

@app.route("/footwear_page")
def footwear_page():
    footwear = get_all_footwear()
    return render_template("footwear.html", footwear=footwear)

@app.route("/accessories_page")
def accessories_page():
    accessories = get_all_accessories()
    return render_template("accessories.html", accessories=accessories)

@app.route("/stickers_page")
def stickers_page():
    stickers = get_all_stickers()
    return render_template("stickers.html", stickers=stickers)

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "GET":
        return render_template("checkout.html")

    try:
        data = request.get_json()
        print("Received checkout data:", data)

        name = data.get("name")
        email = data.get("email")
        address = data.get("address")
        province = data.get("province")
        municipality = data.get("municipality")
        barangay = data.get("barangay")
        items = data.get("items", [])
        total = data.get("total")
        payment_method = data.get("paymentMethod", "N/A")

        if not (name and email and address and items):
            return jsonify({"status": "error", "message": "Missing fields"}), 400

        con_cust = sqlite3.connect("customers.db")
        cur_cust = con_cust.cursor()
        cur_cust.execute("INSERT INTO customers(name, email) VALUES(?, ?)", (name, email))
        con_cust.commit()
        con_cust.close()

        con_order = sqlite3.connect("orders.db")
        cur_order = con_order.cursor()
        
        # Mapping of source names to actual database filenames
        db_map = {
            'tshirt_db': 'tshirt.db',
            'tom_db': 'tom.db',
            'footwear_db': 'footwear.db',
            'accessories_db': 'accessories.db',
            'stickers_db': 'stickers.db',
            # Add other product categories and their corresponding DB files here
        }

        for item in items:
            apparel = item.get("name", "Unknown")
            accessories = item.get("size", "N/A")
            design = item.get("image", "")
            quantity = item.get("quantity", 1)
            price = item.get("price", "0")
            product_id_raw = item.get("id")
            product_source_table = item.get("source")

            # Insert into orders table
            cur_order.execute(
                "INSERT INTO orders(name, email, address, province, municipality, barangay, apparel, accessories, design, quantity, price, payment_method) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (name, email, address, province, municipality, barangay, apparel, accessories, design, quantity, price, payment_method)
            )
            
            # --- STOCK DEDUCTION LOGIC ---
            if product_id_raw is not None and product_source_table and product_source_table in db_map:
                db_filename = db_map[product_source_table]
                table_name_in_db = product_source_table.replace('_db', '')

                try:
                    original_product_id = None
                    if isinstance(product_id_raw, str) and '-' in product_id_raw:
                        original_product_id = int(product_id_raw.split('-')[-1])
                    elif isinstance(product_id_raw, (int, float)):
                        original_product_id = int(product_id_raw)
                    
                    if original_product_id is None:
                        print(f"Error: Unrecognized product ID format for {apparel}: {product_id_raw}. Skipping stock update.")
                        continue

                    con_product_specific = sqlite3.connect(db_filename)
                    cur_product_specific = con_product_specific.cursor()

                    cur_product_specific.execute(f"SELECT stock FROM {table_name_in_db} WHERE id=?", (original_product_id,))
                    current_stock = cur_product_specific.fetchone()
                    
                    if current_stock is not None:
                        new_stock = current_stock[0] - quantity
                        if new_stock < 0:
                            new_stock = 0
                        
                        cur_product_specific.execute(f"UPDATE {table_name_in_db} SET stock=? WHERE id=?", (new_stock, original_product_id))
                        con_product_specific.commit()
                        print(f"Deducted {quantity} from {apparel} (ID: {product_id_raw}, Original ID: {original_product_id}, Source: {table_name_in_db}). New stock: {new_stock}")
                    else:
                        print(f"Warning: Product {apparel} (ID: {product_id_raw}, Original ID: {original_product_id}, Source: {table_name_in_db}) not found for stock update. Check if product exists in '{table_name_in_db}' table with ID {original_product_id}.")
                    con_product_specific.close()
                except sqlite3.OperationalError as op_err:
                    print(f"Database operation error during stock update for {apparel}: {op_err}")
                except Exception as stock_err:
                    print(f"Unexpected error during stock update for {apparel}: {stock_err}")
            else:
                print(f"Warning: Missing product ID, unknown source, or source not mapped for {apparel}, cannot update stock.")

        con_order.commit()
        con_order.close()

        # --- CLEAR THE CART AFTER ORDER ---
        session['cart'] = []
        if 'username' in session:
            con = sqlite3.connect("users.db")
            cur = con.cursor()
            cur.execute("REPLACE INTO user_carts (username, cart) VALUES (?, ?)", (session['username'], json.dumps([])))
            con.commit()
            con.close()

        return jsonify({"status": "success", "redirect": url_for('home')})

    except Exception as e:
        print("Checkout error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Static Pages ---
@app.route("/cart_page")
def cart_page():
    cart_items = session.get('cart', [])
    return render_template("cart_page.html", cart_items=cart_items)

@app.route("/brand")
def brand():
    return render_template("brand.html")

@app.route("/shop")
def shop():
    return render_template("shop.html")

@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/lookbook")
def lookbook():
    return render_template("lookbook.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/allCateg")
def allCateg():
    return render_template("allCateg.html")

# --- User Authentication Routes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['user_logged_in'] = True
            session['admin_logged_in'] = True
            session['username'] = username
            # Optionally set admin name
            session['firstname'] = 'Admin'
            session['lastname'] = ''
            return redirect(url_for('admin_dashboard'))
        else:
            # Check normal users
            con = sqlite3.connect("users.db")
            cur = con.cursor()
            cur.execute("SELECT firstname, lastname FROM users WHERE username=? AND password=?", (username, password))
            user = cur.fetchone()
            con.close()
            if user:
                session['user_logged_in'] = True
                session['username'] = username
                session['firstname'] = user[0]
                session['lastname'] = user[1]
                # Load cart from DB
                con = sqlite3.connect("users.db")
                cur = con.cursor()
                cur.execute("SELECT cart FROM user_carts WHERE username=?", (username,))
                row = cur.fetchone()
                if row and row[0]:
                    session['cart'] = json.loads(row[0])
                else:
                    session['cart'] = []
                con.close()
                return redirect(url_for('home'))
            else:
                flash('Invalid credentials.', 'danger')
    return render_template('admin_login.html', signup=False)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
        else:
            try:
                con = sqlite3.connect("users.db")
                cur = con.cursor()
                cur.execute("INSERT INTO users (firstname, lastname, username, email, password) VALUES (?, ?, ?, ?, ?)",
                            (firstname, lastname, username, email, password))
                con.commit()
                con.close()
                flash('Signup successful! Please log in.', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Username already exists.', 'danger')
    return render_template('admin_login.html', signup=True)

@app.route('/logout', methods=['POST'])
def logout():
    if 'username' in session and 'cart' in session:
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        cur.execute("REPLACE INTO user_carts (username, cart) VALUES (?, ?)",
                    (session['username'], json.dumps(session['cart'])))
        con.commit()
        con.close()
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/admin/update_stock/<category>/<path:name>', methods=['POST'])
def update_stock(category, name):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    stock = request.form.get('stock', type=int)
    # Define a dictionary to map category names to their respective database files
    db_map = {
        'tshirt': 'tshirt.db',
        'tom': 'tom.db',
        'footwear': 'footwear.db',
        'accessories': 'accessories.db',
        'stickers': 'stickers.db'
    }

    db_file = db_map.get(category)
    if db_file and stock is not None:
        try:
            con = sqlite3.connect(db_file)
            cur = con.cursor()
            # The table name within the database is typically the same as the category (lowercase)
            table_name = category 
            cur.execute(f"UPDATE {table_name} SET stock=? WHERE name=?", (stock, name))
            con.commit()
            con.close()
            flash(f"{category.title()} stock updated!", "success")
        except Exception as e:
            flash(f"Error updating {category.title()} stock: {e}", "danger")
    else:
        flash("Invalid update request or category.", "danger")
    return redirect(url_for('admin_dashboard'))


# --- Server Run ---
if __name__ == "__main__":
    init_orders_db()
    init_customers_db()
    init_products_db()
    init_users_db()
    init_user_carts_db()
    
    # Initialize and seed individual product databases
    # Ensure these functions exist in their respective files and manage their own DBs
    init_db()
    seed_products()

    init_tom_db()
    seed_tom()
    init_tshirt_db()
    seed_tshirt()
    init_footwear_db()
    seed_footwear()
    init_accessories_db()
    seed_accessories()
    init_stickers_db()
    seed_stickers()
    app.run(debug=True, host='0.0.0.0', port=5000)