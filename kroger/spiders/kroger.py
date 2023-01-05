# -*- coding: utf-8 -*-
import traceback

import scrapy
from bs4 import BeautifulSoup

KROGER_URL = "https://www.kroger.com"

excluded_list = [
    "fresh fruits & vegetables",
    "meat & seafood",
    "dairy & eggs",
    "frozen foods",
    "beer, wine & liquor",
    "deli",
    "bakery",
    "floral",
    "home"]
page_count = 100


class KrogerSpider(scrapy.Spider):
    name = 'kroger'
    allowed_domains = ['www.kroger.com']
    start_urls = [url % page for page in range(1, page_count) for url in
                  [f'https://www.kroger.com/pl/beverages/{str(i).zfill(2)}?page=%s' for i in range(1, 50)]]

    def parse(self, response, **kwargs):
        try:
            total_number_of_products = response.xpath(
                '//*[@id="content"]/div/div/div/div[3]/div[2]/div[1]/h2//text()').get()
            department = response.xpath(
                '//*[@id="content"]/div/div/div/div[3]/div[2]/div[1]/h1//text()').get()
            try:
                if total_number_of_products is not None:
                    total_number_of_products = int(
                        total_number_of_products.split("results")[0].strip().replace(",", ""))
            except:
                if total_number_of_products is not None:
                    print("url", response.url)
                    print("total_number_of_products", total_number_of_products)
                    print("department", department)
            if department is not None:
                if department.lower() not in excluded_list:
                    department_details = response.xpath('//*[@id="content"]')
                    for row in department_details:
                        product_details = row.xpath('//*[@id="content"]/div/div/div/div[3]/div[2]').get()
                        if product_details:
                            soup = BeautifulSoup(product_details)
                            if soup.findAll('div', attrs={'class': 'flex-grow w-full h-64'}):
                                for div in soup.findAll('div', attrs={'class': 'flex-grow w-full h-64'}):
                                    yield response.follow(url=KROGER_URL + div.find('a')['href'],
                                                          callback=self.parse_product_details,
                                                          meta={"department": department})
        except Exception:
            traceback.print_exc()

    def parse_product_details(self, response):
        try:
            department = response.meta["department"]
            price_symbol = ""
            product_details = response.xpath('//*[@id="content"]')
            discount = ""
            for row in product_details:
                price = row.xpath('//*[@id="content"]/div/div/div[1]/div[2]/div[2]').get()
                if price:
                    soup = BeautifulSoup(price)
                    promotional_decorated = 'kds-Price-promotional kds-Price-promotional--plain kds-Price-promotional--decorated'
                    if soup.findAll('mark', attrs={'class': promotional_decorated}):
                        for mark in soup.findAll('mark', attrs={'class': promotional_decorated}):
                            string = str(mark)
                            if "$" in string:
                                price_symbol = "$"

                    col_items_end_w_full = 'flex flex-col items-end w-full'
                    if soup.findAll('div', attrs={'class': col_items_end_w_full}):
                        for div in soup.findAll('div', attrs={'class': col_items_end_w_full}):
                            price = price_symbol + div.find('data')["value"]

                    promo_banner = 'MiniTag MiniTag--special PurchaseOptions--promoBanner'
                    if soup.findAll('div', attrs={'class': promo_banner}):
                        for div in soup.findAll('div', attrs={'class': promo_banner}):
                            discount = div["aria-label"].replace("Tag:", "")

                if price not in [None, ""]:
                    if len(price) > 10:
                        price = ""
                else:
                    price = ""

                upc = row.xpath('//*[@id="content"]/div/div/div[1]/div[2]/div[2]/div/div[2]/span[2]//text()').get()
                upc_id = ""
                try:
                    if upc:
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

                product_name = row.xpath('//*[@id="content"]/div/div/div[1]/div[2]/div[2]/div/h1//text()').get()
                if product_name is not None:
                    if "kroger" not in str(product_name).lower() and "simple truth" not in str(product_name).lower():
                        product_name = product_name.replace("™", ""). \
                            replace("®", "").replace("©", ""). \
                            replace("℗", "").replace("℠", ""). \
                            replace("§", "")

                        yield {
                            "department": department,
                            "product_name": product_name,
                            "seller_unit": seller_unit,
                            "price": price,
                            "discount": discount,
                            "upc": upc_id,
                            "url": response.url
                        }
        except Exception as e:
            traceback.print_exc()
