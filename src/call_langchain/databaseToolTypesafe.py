from decimal import Decimal
import sqlite3
from langchain_typesafe import Choice, Noul, Score, TypeSafeClassifier, classifier


def init_db():
    conn = sqlite3.connect("sqlite_products.db")  # creates if it doesn't exist
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        type TEXT,
        price INTEGER
    )""")

    seed = [
        ("Galaxy S26", "phone", 479800),
        ("iPhone 17", "phone", 559400),
        ("Xiaomi Redmi 15 Pro", "phone", 280000),
        ("Canon EOS R100", "camera", 335000),
        ("Canon EOS R8", "camera", 934500),
        ("Canon EOS R6 Mark II", "camera", 1399000),
        ("Sony a7 IV", "camera", 1301900),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO products (name, type, price) VALUES (?, ?, ?)", seed
    )

    conn.commit()


def get_products() -> list:
    """Retrieves a list of all products from database. Contains name, type and price."""

    conn = sqlite3.connect("sqlite_products.db")  # creates if it doesn't exist
    conn.row_factory = sqlite3.Row

    print("Retrieving products from database...")
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    return cur.fetchall()


def get_byName(name: str) -> sqlite3.Row:
    """Retrieves a single product from database by its name. Contains name, type and price."""

    conn = sqlite3.connect("sqlite_products.db")  # creates if it doesn't exist
    conn.row_factory = sqlite3.Row

    print("Retrieving products from database...")
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE name = ?", (name,))
    return cur.fetchone()


init_db()


def compare_all():
    products = get_products()

    classifier = TypeSafeClassifier()

    response = classifier.invoke(
        {
            "state": (
                "I'm looking for a cheap, beginner-friendly camera to start a photography hobby."
                "I'm mostly going to take photos."
                # "I'm looking for a camera. I already have a Canon EOS R100 but I'm looking to level-up my photography"
                # "I'll also take video."
            ),
            "questions": {
                "team": Choice(
                    instructions="Which option best matches what the user needs?",
                    criteria={
                        item["name"]: f"Name: {item["name"]} | Product type: {item["type"]} | Price: {
                            item["price"]
                        }"
                        for item in products
                    },
                ),
            },
        }
    )

    print(response)


def compare_one():
    product = get_byName("Canon EOS R100")

    classifier = TypeSafeClassifier()

    response = classifier.invoke(
        {
            "state": (f"I'm looking to get a camera and found this: {product["name"]}"),
            "questions": {
                "team": Choice(
                    instructions="Which option best matches what the user needs?",
                    criteria={
                        item["price"]: f"Name: {item["name"]} | Product type: {item["type"]} | Price: {
                            item["price"]
                        }"
                        for item in products
                    },
                ),
            },
        }
    )

    print(response)


compare_all()
