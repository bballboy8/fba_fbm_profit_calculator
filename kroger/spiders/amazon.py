# -*- coding: utf-8 -*-
from urllib.parse import urlencode

import scrapy

# API = ''  ##Insert Scraperapi API key here. Signup here for free trial with 5,000 requests: https://www.scraperapi.com/signup
##Insert Scraperapi API key here. Signup here for free trial with 10,000 requests: https://app.scrapingant.com/signup
API = #'69b042b0a8904084ab2ff389fb8b5010' expired for jan 2023

AMAZON_URL = 'https://www.amazon.com/'
SCRAPINGANT_URL = 'http://api.scrapingant.com/v2/general?'


# scraperapi
# def get_url(url):
#     payload = {'api_key': API, 'url': url, 'country_code': 'us'}
#     proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
#     return proxy_url

# scrapingant
def get_url(url):
    payload = {'x-api-key': API, 'url': url}
    proxy_url = SCRAPINGANT_URL + urlencode(payload)
    return proxy_url


class AmazonSpider(scrapy.Spider):
    name = 'amazon'

    def start_requests(self):
        for query in self.queries:
            url = AMAZON_URL + 's?' + urlencode({'k': query})
            yield scrapy.Request(url=get_url(url), callback=self.parse_keyword_response, meta={"query": query})

    def parse_keyword_response(self, response):
        products = response.xpath('//*[@data-asin]')
        query = response.meta["query"]
        for product in products:
            asin = product.xpath('@data-asin').extract_first()
            product_url = AMAZON_URL + f"dp/{asin}"
            yield scrapy.Request(url=get_url(product_url), callback=self.parse_product_page,
                                 meta={'asin': asin, "query": query})

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
