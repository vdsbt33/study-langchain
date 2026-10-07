from decimal import Decimal
import sqlite3
from langchain.agents import create_agent


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
    print("Retrieving products from database...")
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    return cur.fetchall()


init_db()


def main():
    agent = create_agent(
        model="claude-sonnet-5-5",
        tools=[get_products],
        system_prompt="You are a helpful assistant. Answer very directly, without any additional information.",
    )

    print("Calling agent...")
    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": "What's the cheapest camera we have?"}
            ]
        }
    )

    print("\n\n", result, "\n\n")
    print(result["messages"][-1].content_blocks)


main()
