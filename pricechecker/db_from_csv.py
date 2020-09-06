import pandas as pd
from pathlib import Path
from datetime import date
from pricechecker.db_tools import \
    select_product_by_id, select_all_products,\
    create_connection


here = Path(__file__).parent

today = str(date.today())

data = pd.read_csv(here/'data.csv')

connection = create_connection(here.parent/'pricechecker.db')
cursor = connection.cursor()
c1 ="""CREATE TABLE IF NOT EXISTS
products(product_id INTEGER PRIMARY KEY, product_name TEXT, desired_price REAL DEFAULT NULL, url_ss TEXT DEFAULT NULL, url_ss_api TEXT DEFAULT NULL)"""
cursor.execute(c1)
c2 ="""CREATE TABLE IF NOT EXISTS
sainsbury_prices(product_id INTEGER,  price_date TEXT, price REAL, FOREIGN KEY(product_id) REFERENCES products(product_id))"""
cursor.execute(c2)
for i in range(len(data)):
    cursor.execute("INSERT INTO products (product_name, desired_price, url_ss, url_ss_api) VALUES (?,?,?,?)",
                   (data.name.loc[i], float(data.desired_price.loc[i]), data.ss_url.loc[i],data.ss_api_url.loc[i]))
cursor.execute("SELECT * FROM products")
db = cursor.fetchall()
print(db)