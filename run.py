import json

import pandas as pd
from scrapy.crawler import CrawlerProcess
from kroger.spiders.kroger import KrogerSpider
from kroger.spiders.amazon import AmazonSpider
from amazon_keepa import keepa_scripts

kroger_data_path = "output/kroger.csv"
amazon_data_path = "output/amazon.csv"
final_profit_data_path = "output/final.csv"


def create_product_list(input_file_path):
    df = pd.read_csv(input_file_path)
    df.seller_unit = df.seller_unit.fillna('')
    df['final_product_name'] = df["product_name"] + ' ' + df["seller_unit"]
    df['final_product_name'] = df['final_product_name'].str.replace("§", "")
    df['final_product_name'] = df['final_product_name'].str.replace("oz", "")
    df['final_product_name'] = df['final_product_name'].str.replace("ct", "")
    df['final_product_name'] = df['final_product_name'].str.replace("lb", "")
    df['final_product_name'] = df['final_product_name'].str.replace("pk", "")
    df['final_product_name'] = df['final_product_name'].str.replace("yd", "")
    product_name_list = list(set(df["product_name"]))
    return product_name_list


def create_profit_report():
    kroger_df = pd.read_csv(kroger_data_path)
    amazon_df = pd.read_csv(amazon_data_path)
    combined_df = pd.merge(kroger_df, amazon_df, on='product_name')
    product_asin_list = list(set(amazon_df["asin"]))
    keep_data_list = []
    for each_asin in product_asin_list:
        final_product_list = json.loads(combined_df.to_json(orient='records'))
        for each_product in final_product_list:
            if each_product["asin"] == each_asin:
                purchase_price = each_product["price"]
                seller_unit = each_product["seller_unit"]
                if purchase_price not in [None, "None"]:
                    asin, fbm, fba = keepa_scripts.search_product(each_asin, purchase_price, seller_unit)
                    # keep_data_list.append({"asin": asin,
                    #                        "FBM": {"profit": fbm["fbm_profit"],
                    #                                "shipping_cost": fbm["shipping_cost"],
                    #                                "packing_materials": fbm["packing_materials"], "labor": fbm["labor"],
                    #                                "referral_fee": fbm["referral_fee"]},
                    #                        "FBA": {"profit": fba["fba_profit"], "shipping_cost": fba["shipping_cost"],
                    #                                "packing_materials": fba["packing_materials"], "labor": fba["labor"],
                    #                                "referral_fee": fba["referral_fee"],
                    #                                "storage_fee": fba["storage_fee"],
                    #                                "small_and_light": fba["small_and_light"]}})
                    if not fbm["fbm_profit"] < 0 and not fba["fba_profit"] < 0:
                        keep_data_list.append(
                            {"asin": asin, "fbm_profit": fbm["fbm_profit"], "fba_profit": fba["fba_profit"]})
    keep_data_df = pd.DataFrame(keep_data_list)
    final_df = pd.merge(combined_df, keep_data_df, on='asin')
    final_df.to_csv(final_profit_data_path, index=False)


if __name__ == '__main__':
    # to start the kroger scrapping
    process = CrawlerProcess({
        'FEED_FORMAT': 'csv',
        'FEED_URI': kroger_data_path})
    process.crawl(KrogerSpider)
    process.start()

    # to start the amazon scrapping
    queries = create_product_list(kroger_data_path)
    process = CrawlerProcess(
        {'FEED_FORMAT': 'csv',
         'FEED_URI': amazon_data_path})
    process.crawl(AmazonSpider, queries=queries)
    process.start()

    # to create the final profit products data
    create_profit_report()
