# -*- coding: utf-8 -*-
from urllib.parse import urlencode

import random
import scrapy

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
]

AMAZON_URL = 'https://www.amazon.com/'

class AmazonSpider(scrapy.Spider):
    name = 'amazon'

    def start_requests(self):
        for query in self.queries:
            url = AMAZON_URL + 's?' + urlencode({'k': query})
            rand_int = random.randint(0, len(user_agent_list)-1)
            user_agent = user_agent_list[rand_int]
            yield scrapy.Request(
                    url=url, 
                    callback=self.parse_keyword_response,
                    meta={"query": query},
                    headers={"User-Agent": user_agent}
                )

    def parse_keyword_response(self, response):
        products = response.xpath('//*[@data-asin]')
        query = response.meta["query"]
        for product in products:
            asin = product.xpath('@data-asin').extract_first()
            product_url = AMAZON_URL + f"dp/{asin}"
            rand_int = random.randint(0, len(user_agent_list)-1)
            user_agent = user_agent_list[rand_int]

            yield scrapy.Request(
                    url=product_url, 
                    callback=self.parse_product_page,
                    meta={'asin': asin, "query": query},
                    headers={"User-Agent": user_agent}
                )

        # for enabling pagination
        # next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        # if next_page:
        #     url = urljoin("https://www.amazon.com", next_page)
        #     yield scrapy.Request(url=url, callback=self.parse_keyword_response)

    def parse_product_page(self, response):
        asin = response.meta['asin']
        query = response.meta['query']
        title = response.xpath('//*[@id="productTitle"]/text()').extract_first()
        if title:
            result = {'asin': asin, 'Title': title}
            each_product_name_list = query.lower().split(" ")
            if all(word in result["Title"].lower() for word in each_product_name_list):
                yield {"asin": result["asin"],
                       "product_name": query,
                       "amazon_product_name": result["Title"].strip(),
                       "amazon_product_url": response.url}
