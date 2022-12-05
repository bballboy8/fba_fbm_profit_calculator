# -*- coding: utf-8 -*-
import traceback
import scrapy
from bs4 import BeautifulSoup

excluded_list = [
    "fresh fruits & vegetables"
    , "meat & seafood"
    , "dairy & eggs"
    , "frozen foods"
    , "beer, wine & liquor"
    , "deli"
    , "bakery"
    , "floral"
    , "home"]
page_count = 100


class KrogerSpider(scrapy.Spider):
    name = 'kroger'
    allowed_domains = ['www.kroger.com']
    start_urls = [url % page for page in range(1, page_count) for url in
                  ['https://www.kroger.com/pl/beverages/01?page=%s', 'https://www.kroger.com/pl/beverages/02?page=%s',
                   'https://www.kroger.com/pl/beverages/03?page=%s', 'https://www.kroger.com/pl/beverages/04?page=%s',
                   'https://www.kroger.com/pl/beverages/05?page=%s', 'https://www.kroger.com/pl/beverages/06?page=%s',
                   'https://www.kroger.com/pl/beverages/07?page=%s', 'https://www.kroger.com/pl/beverages/08?page=%s',
                   'https://www.kroger.com/pl/beverages/09?page=%s', 'https://www.kroger.com/pl/beverages/10?page=%s',
                   'https://www.kroger.com/pl/beverages/11?page=%s', 'https://www.kroger.com/pl/beverages/12?page=%s',
                   'https://www.kroger.com/pl/beverages/13?page=%s', 'https://www.kroger.com/pl/beverages/14?page=%s',
                   'https://www.kroger.com/pl/beverages/15?page=%s', 'https://www.kroger.com/pl/beverages/16?page=%s',
                   'https://www.kroger.com/pl/beverages/17?page=%s', 'https://www.kroger.com/pl/beverages/18?page=%s',
                   'https://www.kroger.com/pl/beverages/19?page=%s', 'https://www.kroger.com/pl/beverages/20?page=%s',
                   'https://www.kroger.com/pl/beverages/21?page=%s', 'https://www.kroger.com/pl/beverages/22?page=%s',
                   'https://www.kroger.com/pl/beverages/23?page=%s', 'https://www.kroger.com/pl/beverages/24?page=%s',
                   'https://www.kroger.com/pl/beverages/25?page=%s', 'https://www.kroger.com/pl/beverages/26?page=%s',
                   'https://www.kroger.com/pl/beverages/27?page=%s', 'https://www.kroger.com/pl/beverages/28?page=%s',
                   'https://www.kroger.com/pl/beverages/29?page=%s', 'https://www.kroger.com/pl/beverages/30?page=%s',
                   'https://www.kroger.com/pl/beverages/31?page=%s', 'https://www.kroger.com/pl/beverages/32?page=%s',
                   'https://www.kroger.com/pl/beverages/33?page=%s', 'https://www.kroger.com/pl/beverages/34?page=%s',
                   'https://www.kroger.com/pl/beverages/35?page=%s', 'https://www.kroger.com/pl/beverages/36?page=%s',
                   'https://www.kroger.com/pl/beverages/37?page=%s', 'https://www.kroger.com/pl/beverages/38?page=%s',
                   'https://www.kroger.com/pl/beverages/39?page=%s', 'https://www.kroger.com/pl/beverages/40?page=%s',
                   'https://www.kroger.com/pl/beverages/41?page=%s', 'https://www.kroger.com/pl/beverages/42?page=%s',
                   'https://www.kroger.com/pl/beverages/43?page=%s', 'https://www.kroger.com/pl/beverages/44?page=%s',
                   'https://www.kroger.com/pl/beverages/45?page=%s', 'https://www.kroger.com/pl/beverages/46?page=%s',
                   'https://www.kroger.com/pl/beverages/47?page=%s', 'https://www.kroger.com/pl/beverages/48?page=%s',
                   'https://www.kroger.com/pl/beverages/49?page=%s']]

    def parse(self, response, **kwargs):
        try:
            total_number_of_products = response.xpath(
                '//*[@id="content"]/div/div/div/div[3]/div[2]/div[1]/h2//text()').get()
            department = response.xpath(
                '//*[@id="content"]/div/div/div/div[3]/div[2]/div[1]/h1//text()').get()
            try:
                total_number_of_products = int(
                    total_number_of_products.split("results")[0].strip().replace(",", ""))
            except:
                print("url", response.url)
                print("total_number_of_products", total_number_of_products)
                print("department", department)
            if department is not None:
                if department.lower() not in excluded_list:
                    department_details = response.xpath(
                        '//*[@id="content"]')
                    for row in department_details:
                        product_details = row.xpath('//*[@id="content"]/div/div/div/div[3]/div[2]').get()
                        if product_details:
                            soup = BeautifulSoup(product_details)
                            if soup.findAll('div', attrs={'class': 'flex-grow w-full h-64'}):
                                for div in soup.findAll('div', attrs={'class': 'flex-grow w-full h-64'}):
                                    yield response.follow(url="https://www.kroger.com" + div.find('a')['href'],
                                                          callback=self.parse_product_details,
                                                          meta={"department": department})

        except Exception as e:
            traceback.print_exc()

    def parse_product_details(self, response):
        try:
            department = response.meta["department"]
            price_symbol = ""
            product_details = response.xpath(
                '//*[@id="content"]')
            discount = ""
            for row in product_details:
                product_name = row.xpath('//*[@id="content"]/div/div/div[1]/div[2]/div[2]/div/h1//text()').get()
                price = row.xpath('//*[@id="content"]/div/div/div[1]/div[2]/div[2]').get()
                if price:
                    soup = BeautifulSoup(price)
                    if soup.findAll('mark', attrs={
                        'class': 'kds-Price-promotional kds-Price-promotional--plain kds-Price-promotional--decorated'}):
                        for mark in soup.findAll('mark', attrs={
                            'class': 'kds-Price-promotional kds-Price-promotional--plain kds-Price-promotional--decorated'}):
                            string = str(mark)
                            if "$" in string:
                                price_symbol = "$"
                    if soup.findAll('div', attrs={'class': 'flex flex-col items-end w-full'}):
                        for div in soup.findAll('div', attrs={'class': 'flex flex-col items-end w-full'}):
                            price = price_symbol + div.find('data')["value"]
                    if soup.findAll('div',
                                    attrs={'class': 'MiniTag MiniTag--special PurchaseOptions--promoBanner'}):
                        for div in soup.findAll('div', attrs={
                            'class': 'MiniTag MiniTag--special PurchaseOptions--promoBanner'}):
                            discount = div["aria-label"].replace("Tag:", "")

                if price not in [None, ""]:
                    if len(price) > 10:
                        price = ""
                else:
                    price = ""
                upc = row.xpath('//*[@id="content"]/div/div/div[1]/div[2]/div[2]/div/div[2]/span[2]//text()').get()
                upc_id = ""
                if upc:
                    try:
                        upc_id = str(upc).split(":")[1].strip()
                    except:
                        upc_id = ""
                if upc_id == "":
                    upc_id = str(response.url).split("/")[-1]
                    if "?" in upc_id:
                        upc_id = str(upc_id).split("?")[0]
                seller_unit = row.xpath('//*[@id="ProductDetails-sellBy-unit"]//text()').get()
                if not seller_unit:
                    seller_unit = ""
                if product_name is not None:
                    if "kroger" not in str(product_name).lower() and "simple truth" not in str(product_name).lower():
                        product_name = product_name.replace("™", ""). \
                            replace("®", "").replace("©", ""). \
                            replace("℗", "").replace("℠", ""). \
                            replace("§", "")

                        yield {"department": department,
                               "product_name": product_name,
                               "seller_unit": seller_unit,
                               "price": price,
                               "discount": discount,
                               "upc": upc_id,
                               "url": response.url}


        except Exception as e:
            traceback.print_exc()
