import scrapy
import json
import pandas as pd
from pathlib import Path
from datetime import date
import sqlite3
from pricechecker.db_tools import \
    select_product_by_id, select_all_products,\
    create_connection


here = Path(__file__).parent

today = str(date.today())

data = pd.read_csv(here.parent/'data.csv')

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

#print(data)
#type(data)
class SainsburySpider(scrapy.Spider):
    name = "sainsburys"

    #start_urls = list(data.ss_api_url)

    def start_requests(self):
        start_urls = list(data.ss_api_url)

        for url in start_urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 )

    def parse(self, response):


        raw_data = response.body
        web_data = json.loads(raw_data)
        id = web_data['products'][0]['product_uid']
        name = web_data['products'][0]['name']
        price = web_data['products'][0]['retail_price']['price']
        print("***************** YO, I GOT THE PRICE", name, price)





        #if price < desired_price:
        #   print("+++++++++++++ON DISCOUNT++++++++++++++++")
        #else:
        #    print("--------------NOT ON DISCOUNT---------------")

#        with open('data.csv', 'w+') as file:



