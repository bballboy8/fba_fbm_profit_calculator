import formulas


def amazon_device_accessories(list_price):
    func = formulas.Parser().ast('=MAX(0.45 *list_price, 0.3)')[1].compile()
    return func(list_price)


def amazon_explore(list_price):
    func = formulas.Parser().ast('=max(0.3*list_price,2)')[1].compile()
    return func(list_price)


def applicances_compact(list_price):
    func = formulas.Parser().ast('=max(if(list_price<=300,list_price*0.15,45+(list_price-300)*0.08),0.3)')[1].compile()
    return func(list_price)


def applicances_full_size(list_price):
    func = formulas.Parser().ast('=max(0.08*list_price,0.3)')[1].compile()
    return func(list_price)


def automotive_and_powersports(list_price):
    func = formulas.Parser().ast('=max(0.12*list_price,0.3)')[1].compile()
    return func(list_price)


def base_equipment_power_tools(list_price):
    func = formulas.Parser().ast('=max(0.12*list_price,0.3)')[1].compile()
    return func(list_price)


def baby_products(list_price):
    func = formulas.Parser().ast('=max(if(list_price<=10,list_price*0.08,list_price*0.15),0.3)')[1].compile()
    return func(list_price)


def backpacks_handbags_and_luggage(list_price):
    func = formulas.Parser().ast('=max(0.15*list_price,0.3)')[1].compile()
    return func(list_price)


def beauty_health_and_personal_care(list_price):
    func = formulas.Parser().ast('=max(if(list_price<=10,list_price*0.08,list_price*0.15),0.3)')[1].compile()
    return func(list_price)


def business_industrial_and_scientific_supplies(list_price):
    func = formulas.Parser().ast('=max(0.12*list_price,0.3)')[1].compile()
    return func(list_price)


def clothing_and_accessories(list_price):
    func = formulas.Parser().ast('=max(0.17*list_price,0.3)')[1].compile()
    return func(list_price)


def collectibles_coins(list_price):
    func = formulas.Parser().ast(
        '=max(if(list_price<=250,list_price*0.15,if(list_price<=1000,37.5+(list_price-250)*0.1,112.5+(list_price-1000)*0.06)),0.3)')[
        1].compile()
    return func(list_price)


def collectibles_entertainment(list_price):
    func = formulas.Parser().ast(
        '=max(if(list_price<=100,list_price*0.15,if(list_price<=1000,15+(list_price-100)*0.1,105+(list_price-1000)*0.06)),0.3)')[
        1].compile()
    return func(list_price)


def collectibles_sports(list_price):
    func = formulas.Parser().ast(
        '=max(if(list_price<=100,list_price*0.15,if(list_price<=1000,15+(list_price-100)*0.1,105+(list_price-1000)*0.06)),0.3)')[
        1].compile()
    return func(list_price)


def computers(list_price):
    func = formulas.Parser().ast('=max(0.08*list_price,0.3)')[1].compile()
    return func(list_price)


def consumer_electronics(list_price):
    func = formulas.Parser().ast('=max(0.08*list_price,0.3)')[1].compile()
    return func(list_price)


def electronics_accessories(list_price):
    func = formulas.Parser().ast('=max(if(list_price<=100,list_price*0.15,15+(list_price-100)*0.08),0.3)')[1].compile()
    return func(list_price)


def eyewear(list_price):
    func = formulas.Parser().ast('=max(0.15*list_price,0.3)')[1].compile()
    return func(list_price)


def fine_art(list_price):
    func = formulas.Parser().ast(
        '=max(if(list_price<=100,list_price*0.2,if(list_price<=1000,20+(list_price-100)*0.15,if(list_price<=5000,155+(list_price-1000)*0.1,555+(list_price-5000)*0.05))),1)')[
        1].compile()
    return func(list_price)


def footwear(list_price):
    func = formulas.Parser().ast('=max(0.15*list_price,0.3)')[1].compile()
    return func(list_price)


def furniture(list_price):
    func = formulas.Parser().ast('=max(if(list_price<=200,list_price*0.15,30+(list_price-200)*0.1),0.3)')[1].compile()
    return func(list_price)


def gift_cards(list_price):
    func = formulas.Parser().ast('=max(0.2*list_price,0.3)')[1].compile()
    return func(list_price)


def grocery_and_gourmet(list_price):
    func = formulas.Parser().ast('=max(if(list_price<=15,list_price*0.08,list_price*0.15),0.3)')[1].compile()
    return func(list_price)


def home_and_kitchen(list_price):
    func = formulas.Parser().ast('=max(0.15*list_price,0.3)')[1].compile()
    return func(list_price)


def jewelry(list_price):
    func = formulas.Parser().ast('=max(if(list_price<=250,list_price*0.2,50+(list_price-250)*0.05),0.3)')[1].compile()
    return func(list_price)


def lawn_and_garden(list_price):
    func = formulas.Parser().ast('=max(0.15*list_price,0.3)')[1].compile()
    return func(list_price)


def lawn_mowers_and_snow_throwers(list_price):
    func = formulas.Parser().ast('=max(if(list_price<=500,list_price*0.15,list_price*0.08),0.3)')[1].compile()
    return func(list_price)


def media(list_price):
    func = formulas.Parser().ast('=MAX(1.8+0.15*list_price,0.3)')[1].compile()
    return func(list_price)


def musical_instruments_and_av_production(list_price):
    func = formulas.Parser().ast('=max(0.15*list_price,0.3)')[1].compile()
    return func(list_price)


def office_products(list_price):
    func = formulas.Parser().ast('=max(0.15*list_price,0.3)')[1].compile()
    return func(list_price)


def pet_supplies(list_price):
    func = formulas.Parser().ast('=max(0.15*list_price,0.3)')[1].compile()
    return func(list_price)


def sports_and_outdoors(list_price):
    func = formulas.Parser().ast('=max(0.15*list_price,0.3)')[1].compile()
    return func(list_price)


def tires(list_price):
    func = formulas.Parser().ast('=max(0.1*list_price,0.3)')[1].compile()
    return func(list_price)


def tools_and_home_improvement(list_price):
    func = formulas.Parser().ast('=max(0.15*list_price,0.3)')[1].compile()
    return func(list_price)


def toys_and_games(list_price):
    func = formulas.Parser().ast('=max(0.15*list_price,0.3)')[1].compile()
    return func(list_price)


def video_games_and_gaming_accessories(list_price):
    func = formulas.Parser().ast('=0.15*list_price')[1].compile()
    return func(list_price)


def video_game_consoles(list_price):
    func = formulas.Parser().ast('=0.08*list_price')[1].compile()
    return func(list_price)


def watches(list_price):
    func = formulas.Parser().ast('=max(if(list_price<=1500,list_price*0.16,240+(list_price-1500)*0.03),0.3)')[
        1].compile()
    return func(list_price)


def everything_else(list_price):
    func = formulas.Parser().ast('=max(0.15*list_price,0.3)')[1].compile()
    return func(list_price)
