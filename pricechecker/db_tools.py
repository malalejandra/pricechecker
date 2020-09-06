import sqlite3
from sqlite3 import Error


def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_all_products(conn):

    cur = conn.cursor()
    cur.execute("SELECT * FROM products")

    rows = cur.fetchall()
    for row in rows:
        print(row)


def select_product_by_id(conn, id):

    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE product_id=?", (id,))

    rows = cur.fetchall()

    for row in rows:
        print(row)


def main():
    database = r"/home/alexa/Projects/Python/pricechecker/pricechecker/pricechecker.db"
    conn = create_connection(database)
    print("1. Query products by id")
    select_product_by_id(conn, 1)

    print("2. Query all products")
    select_all_products(conn)


if __name__ == '__main__':
    main()