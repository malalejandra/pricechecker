import scrapy
import json

class SainsburySpider(scrapy.Spider):
    name = "vivino"
    start_urls = ['https://www.vivino.com/']

    headers = {
        "Host": "www.sainsburys.co.uk",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv: 79.0) Gecko / 20100101 Firefox / 79.0",
        "Accept": "application/json",
        "Accept-Language": "en-GB, en; q = 0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
    }

    def parse(self, response):
        urls = [
            'https://www.sainsburys.co.uk/groceries-api/gol-services/product/v1/product?filter[product_seo_url]=gb%2Fgroceries%2Fbrancott-estate-sauvignon-blanc-75cl&include[ASSOCIATIONS]=true&include[DIETARY_PROFILE]=true',
            'https://www.sainsburys.co.uk/groceries-api/gol-services/product/v1/product?filter[product_seo_url]=gb%2Fgroceries%2Fsauvignon-blanc-%2Foyster-bay-sauvignon-blanc-75cl&include[ASSOCIATIONS]=true&include[DIETARY_PROFILE]=true',
            'https://www.sainsburys.co.uk/groceries-api/gol-services/product/v1/product?filter[product_seo_url]=gb%2Fgroceries%2Fsauvignon-blanc-%2Fvilla-maria-private-bin-sauvignon-blanc-75cl&include[ASSOCIATIONS]=true&include[DIETARY_PROFILE]=true'
                ]
        for url in urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse_api,
                                 headers=self.headers)

    def parse_api(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        name = data['products'][0]['name']
        price = data['products'][0]['retail_price']['price']
        print("***************** YO, I GOT THE PRICE", name, price)


