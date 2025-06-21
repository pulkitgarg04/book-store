import sqlite3
from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "your-secret-key"
Session(app)

def get_db_connection():
    conn = sqlite3.connect("store.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    categories = conn.execute("SELECT DISTINCT category FROM books").fetchall()
    books = conn.execute("SELECT * FROM books ORDER BY title LIMIT 12").fetchall()
    conn.close()
    return render_template("index.html", books=books, categories=categories)

@app.route("/search")
def search():
    query = request.args.get("q", "")
    category = request.args.get("category", "")
    conn = get_db_connection()
    categories = conn.execute("SELECT DISTINCT category FROM books").fetchall()
    
    sql = "SELECT * FROM books WHERE title LIKE ?"
    params = [f"%{query}%"]
    if category:
        sql += " AND category = ?"
        params.append(category)
    
    books = conn.execute(sql, params).fetchall()
    conn.close()
    return render_template("search.html", books=books, categories=categories, query=query)

@app.route("/cart", methods=["GET", "POST"])
def cart():
    if "cart" not in session:
        session["cart"] = []
    
    # Temporary fix: Clear cart if it contains strings
    if any(isinstance(item, str) for item in session["cart"]):
        session["cart"] = []
        session.modified = True
        flash("Cart was reset due to invalid data", "error")
    
    if request.method == "POST":
        book_id = request.form.get("id")
        quantity = int(request.form.get("quantity", 1))
        if book_id:
            session["cart"].append({"id": book_id, "quantity": quantity})
            session.modified = True
        return redirect("/cart")

    conn = get_db_connection()
    books = []
    if session["cart"]:
        try:
            book_ids = [item["id"] for item in session["cart"]]
            placeholders = ",".join(["?"] * len(book_ids))
            books = conn.execute(f"SELECT * FROM books WHERE id IN ({placeholders})", book_ids).fetchall()
        except TypeError:
            session["cart"] = []
            session.modified = True
            flash("Invalid cart data detected. Cart has been reset.", "error")
    conn.close()
    return render_template("cart.html", books=books, cart=session["cart"])

@app.route("/cart/remove/<book_id>")
def remove_from_cart(book_id):
    session["cart"] = [item for item in session["cart"] if item["id"] != book_id]
    session.modified = True
    return redirect("/cart")

@app.route("/cart/update", methods=["POST"])
def update_cart():
    for item in session["cart"]:
        quantity = request.form.get(f"quantity_{item['id']}")
        if quantity:
            item["quantity"] = int(quantity)
    session.modified = True
    return redirect("/cart")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            flash("Logged in successfully!", "success")
            return redirect("/")
        flash("Invalid credentials", "error")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password))
            )
            conn.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect("/login")
        except sqlite3.IntegrityError:
            flash("Username already exists", "error")
        finally:
            conn.close()
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect("/")

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if "user_id" not in session:
        flash("Please log in to checkout", "error")
        return redirect("/login")
    
    if request.method == "POST":
        # Process payment (simplified)
        session["cart"] = []
        flash("Purchase completed successfully!", "success")
        return redirect("/")
    
    conn = get_db_connection()
    books = []
    if session["cart"]:
        book_ids = [item["id"] for item in session["cart"]]
        placeholders = ",".join(["?"] * len(book_ids))
        books = conn.execute(f"SELECT * FROM books WHERE id IN ({placeholders})", book_ids).fetchall()
    conn.close()
    return render_template("checkout.html", books=books, cart=session["cart"])

if __name__ == "__main__":
    app.run(debug=True)