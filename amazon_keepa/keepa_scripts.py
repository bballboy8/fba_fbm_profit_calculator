from datetime import datetime
from importlib import import_module

import keepa as keepa

from amazon_keepa.constants import constant_values

ACCESS_KEY = "8uo78hvu8m0i4con694ij5g0jbi7kcck6hrmmh8dr4o61o38t0c1l4c3ppm90kn7"


def get_timestamp(keepa_minutes: int) -> int:
    return (keepa_minutes + 21564000) * 60000


def get_dimension(millimeters: int) -> float:
    return millimeters / 25.4


def get_weight(grams: int) -> float:
    return grams / 454


def get_dimensional_weight(length: float, width: float, height: float) -> float:
    return length * width * height / 166


def requires_multipack(quantity: int) -> bool:
    return quantity > 1


def fbm(shipping_weight, length, width, height, cons,
        constant_values, category, purchase_price, list_price):
    shipping_cost = None
    packing_materials = None
    labor = None
    ref_fee = None

    total_costs = None
    profit = None
    if shipping_weight >= 1 and cons != 0:
        weight = round(length * width * height / cons)
        print(weight)
        max_value = max([shipping_weight, weight])
        print(max_value)
        shipping_cost = float(
            min(constant_values['shipping'], key=lambda x: abs(x["weight_in_pounds"] - max_value))["cost"])
    else:
        shipping_cost = float(
            min(constant_values['shipping'], key=lambda x: abs(x["weight_in_pounds"] - shipping_weight))["cost"])

    packing_materials = constant_values['other_constants']['packing_tape'] / constant_values['other_constants'][
        'packages_per_roll'] \
                        + constant_values['other_constants']['paper'] / 4 + constant_values['other_constants'][
                            'ink'] / 4 \
                        + constant_values['other_constants']['packing_envelope_box']

    labor = constant_values['other_constants']['pack_time'] / 60 * constant_values['other_constants']['labor']

    ref_fee = 0
    for each_item in constant_values['categories']:
        if str(category) in each_item["category_id_list"]:
            function_name = each_item["function"]
            function = getattr(import_module("amazon_keepa.category_utils"), function_name)
            ref_fee = function(list_price)
    total_costs = shipping_cost + packing_materials + labor + ref_fee + purchase_price

    profit = list_price - total_costs

    return profit, shipping_cost, packing_materials, labor, ref_fee, purchase_price


def fba(storage_months, shipping_weight, length, width, height,
        constant_values, category, purchase_price, list_price, multipack, bubble_wrapping, plastic_bag):
    shipping_cost = None
    packing_materials = None
    labor = None
    storage_fee = 0
    size_tier = ''
    small_and_light = False

    total_costs = None
    profit = None

    pm_term_1 = constant_values['other_constants']['label'] + constant_values['other_constants']['ink'] / 44

    pm_term_2 = shipping_weight / 50 * constant_values['other_constants']['paper']

    pm_term_3 = constant_values['other_constants']['packing_envelope_box'] if multipack else 0

    pm_term_3 = constant_values['other_constants']['packing_envelope_box'] if multipack else 0

    pm_term_4 = (width * 2 + height * 2) / 12 * constant_values['other_constants'][
        'bubble_wrap'] if bubble_wrapping else 0

    pm_term_5 = constant_values['other_constants']['packing_envelope_box'] if plastic_bag else 0

    packing_materials = pm_term_1 + pm_term_2 + pm_term_3 + pm_term_4 + pm_term_5

    l_term_1 = shipping_weight / 50 * constant_values['other_constants']['labor'] * constant_values['other_constants'][
        'pack_time_50lb_box'] / 60

    l_term_2 = constant_values['other_constants']['multipack_time'] / 60 * constant_values['other_constants'][
        'labor'] if multipack else 0

    l_term_3 = constant_values['other_constants']['bubble_wrap_time'] / 60 * constant_values['other_constants'][
        'labor'] if bubble_wrapping else 0

    l_term_4 = constant_values['other_constants']['multipack_time'] / 60 * constant_values['other_constants'][
        'labor'] if plastic_bag else 0

    labor = l_term_1 + l_term_2 + l_term_3 + l_term_4

    ref_fee = 0
    for each_item in constant_values['categories']:
        if str(category) in each_item["category_id_list"]:
            function_name = each_item["function"]
            function = getattr(import_module("amazon_keepa.category_utils"), function_name)
            ref_fee = function(list_price)

    # small and light:

    small_and_light = shipping_weight <= 3 and length <= 18 and width <= 14 and height <= 8 and list_price <= 10

    # shipping cost:

    if not small_and_light:

        for parameter in constant_values['size']:
            if length <= parameter['length'] \
                    and width <= parameter['width'] \
                    and height <= parameter['height'] \
                    and shipping_weight <= parameter['weight']:

                shipping_cost = parameter['fulfillment_cost'] + shipping_weight * constant_values['other_constants'][
                    'Shipment_Warehouse']
                size_tier = parameter['size_tier']

                break
            else:
                continue

    else:

        for parameter in constant_values['size']:

            if length <= parameter['length'] \
                    and width <= parameter['width'] \
                    and height <= parameter['height'] \
                    and shipping_weight <= parameter['weight']:

                shipping_cost = parameter['small_and_light_fc'] + shipping_weight * constant_values['other_constants'][
                    'Shipment_Warehouse']
                size_tier = parameter['size_tier']

                break

            else:

                continue

    month = datetime.now().month

    if 'Standard' in size_tier and month <= 9:

        storage_fee = 0.75

    elif 'Standard' in size_tier and month >= 10:

        storage_fee = 2.4

    elif 'Oversize' in size_tier and month >= 10:

        storage_fee = 1.2

    else:

        storage_fee = 0.48

    storage_fee = (storage_fee * storage_months * length / 12 * width / 12 * height / 12) / 2
    total_costs = shipping_cost + packing_materials + labor + ref_fee + storage_fee + purchase_price

    profit = list_price - total_costs

    return profit, shipping_cost, packing_materials, labor, ref_fee, storage_fee, small_and_light, purchase_price


def search_product(query: str, purchase_price: float, seller_unit: str):
    api = keepa.Keepa(ACCESS_KEY)
    products = api.query(query, stats=180)
    interesting_products = [product for product in products if 0 < product["stats"]["salesRankDrops180"] >= 1]
    fbm_parameters, fba_parameters = None, None
    if interesting_products:
        length = interesting_products[0]["packageLength"]
        width = interesting_products[0]["packageWidth"]
        height = interesting_products[0]["packageHeight"]
        weight = interesting_products[0]["packageWeight"]
        try:
            list_price = interesting_products[0]["stats_parsed"]["current"]["AMAZON"]
        except:
            list_price = interesting_products[0]["stats_parsed"]["current"]["NEW"]
        quantity = interesting_products[0]["numberOfItems"]
        if quantity in [-1]:
            quantity = 1
        if "pk" in seller_unit or "ct" in seller_unit or "oz" in seller_unit:
            seller_unit = float(seller_unit.split(" ")[0])
            quantity = quantity / seller_unit
        category = interesting_products[0]["categories"][0]
        purchase_price = quantity * float(str(purchase_price).replace("$", ""))
        storage_months = 6
        bubble_wrapping = True
        plastic_bag = False
        cons = quantity
        fbm_profit, shipping_cost, packing_materials, labor, ref_fee, purchase_price = fbm(
            get_weight(weight),
            get_dimension(length),
            get_dimension(width),
            get_dimension(height),
            cons,
            constant_values,
            category,
            purchase_price,
            list_price)

        fbm_parameters = {"fbm_profit": fbm_profit, "shipping_cost": shipping_cost,
                          "packing_materials": packing_materials, "labor": labor,
                          "referral_fee": ref_fee, "purchase_price": purchase_price}
        print(fbm_parameters)

        fba_profit, shipping_cost, packing_materials, labor, ref_fee, storage_fee, small_and_light, purchase_price = fba(
            storage_months,
            get_weight(weight),
            get_dimension(length),
            get_dimension(width),
            get_dimension(height),
            constant_values,
            category,
            purchase_price,
            list_price,
            requires_multipack(quantity),
            bubble_wrapping,
            plastic_bag)

        fba_parameters = {"fba_profit": fba_profit, "shipping_cost": shipping_cost,
                          "packing_materials": packing_materials, "labor": labor,
                          "referral_fee": ref_fee,
                          "storage_fee": storage_fee, "small_and_light": small_and_light,
                          "purchase_price": purchase_price}
        print(fba_parameters)
    else:
        print(f"Interesting Product not found!")
    return query, fbm_parameters, fba_parameters
