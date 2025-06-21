import sqlite3

conn = sqlite3.connect("store.db")
query = conn.query()

query.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    image_url TEXT NOT NULL,
    description TEXT
)
""")

query.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

query.executescript("""
INSERT OR IGNORE INTO books (title, author, category, price, image_url, description) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 9.99, 'https://upload.wikimedia.org/wikipedia/commons/7/7a/The_Great_Gatsby_Cover_1925_Retouched.jpg', 'A classic novel about the American Dream'),
('1984', 'George Orwell', 'Fiction', 12.99, 'https://m.media-amazon.com/images/I/81+LDW4qePL._UF1000,1000_QL80_.jpg', 'A dystopian novel about surveillance and control'),
('Clean Code', 'Robert C. Martin', 'Technology', 39.99, 'https://images-na.ssl-images-amazon.com/images/I/41jEbK-jG+L._SX376_BO1,204,203,200_.jpg', 'A handbook of software craftsmanship')
""")

conn.commit()
conn.close()