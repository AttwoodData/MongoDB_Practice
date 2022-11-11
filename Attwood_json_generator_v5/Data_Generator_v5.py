# Import necessary packages

import pandas as pd
import numpy as np
import csv
from datetime import date, datetime, timedelta
import re
# random.seed(42)

def sees_docs(customers=100, products=50):
    # ------------------------------------------------------
    # Define top-level variables

    company_age = 365*4
    company_founded = date.today()-timedelta(days = company_age)


    # -----------------------------------------------------
    # Define functions without internal dependencies

    def random_phone_num(count=1):
        def phone_num():
            _area_code = str(np.random.randint(201, 800))
            _second_three = str(np.random.randint(201, 1000))
            _last_four = str(np.random.randint(1000, 10000))
            return _area_code+"-"+_second_three+"-"+_last_four 
        if count == 1:  
            return phone_num()

        else:
            random_phone_num_list =[]
            for i in range(count):
                random_phone_num_list.append(phone_num())
            return random_phone_num_list


    def later_date():
        return date.today()+timedelta(days = np.random.randint(30, 1200))


    def hex_key(digits=6):
        hex_key = ""
        for i in range(digits):
            hex_key += str(np.random.choice(['0','1','2','3','4','5','6','7',
                                             '8','9','A','B','C','D','E','F']))
        return hex_key


    def days_between(d1, d2):
        '''Credit: Fred Foo, Stack Overkflow'''
        d1 = datetime.strptime(str(d1), "%Y-%m-%d")
        d2 = datetime.strptime(str(d2), "%Y-%m-%d")
        return abs((d2 - d1).days)


    def field_decider(a_list, prob=0.5):
            values = [0, 1]
            decider = np.random.choice(values, p=(1-prob,prob))
            if decider > 0:
                return np.random.choice(a_list)
            else:
                return "None"


    # ----------------------------------------------
    # Read in data for generating customer records

    # First names from included file
    with open("first_names.csv") as my_file:
        first_names = my_file.read().split()

    # Surnames from included file
    with open("last_names.csv") as my_file:
        last_names = my_file.read().split()
    last_names = [i.title() for i in last_names]

    # Street names from included file
    with open("streets.csv") as my_file:
        streets = my_file.read().splitlines()
    streets = [i.title() for i in streets]

    # City, state, and zip code tuples
    with open("city_state_zip.csv") as my_file:
        city_state_zip = my_file.read().splitlines()
    city_state_zip = [tuple(i.split(', ')) for i in city_state_zip]


    # ---------------------------------------------
    # Build customer_collection without orders added yet

    # ---Function begin---
    def customer_record():
        _loc_index = np.random.randint(0, len(city_state_zip)-1)
        _location = city_state_zip[_loc_index] 
        _first_name = np.random.choice(first_names)
        _last_name = np.random.choice(last_names)

        def construct_address():
            _address = {}
            _address["street_address"] = str(np.random.randint(1,12000))+" "+np.random.choice(streets)
            _address["city"] = _location[0].title()
            _address["state"] = _location[1]
            _address["zip"] = _location[2]
            _address["address_id"] = hex_key(4)
            return _address


        def construct_payment():
            def construct_number():
                card_number = ""
                for i in range(4):
                    card_number += str(np.random.randint(1000, 9999))+"-"
                return card_number[:-1]


            card_types = ["Visa", "Mastercard", "Discover", "American Express"]

            _payment = {}
            _payment["card_number"] = construct_number()
            _payment["card_type"] = np.random.choice(card_types)
            _payment["exp_date"] = later_date()
            _payment["cvv"] = np.random.randint(100,999)

            _payment["billing_address"] = _record["primary_address"] 
            return _payment

        _record = {}
        _record["first_name"] = _first_name
        _record["last_name"] = _last_name
        _record["phone"] = random_phone_num()
        _record["acct_created"] = date.today() - timedelta(days = np.random.randint(1, 720))
        _record["cust_id"] = _first_name[:2].lower() + _last_name[:4].lower() + _record["phone"][-4:]
        
        _record["shipping_addresses"] = []

        for i in range(np.random.randint(1,4)):
            _record["shipping_addresses"].append(construct_address())
       
        _record["primary_address"] = _record["shipping_addresses"][0] 

        _record["payment_method"] = construct_payment()

        return _record
    # ---Function end---

    # create the customer documents and add them to the collection
    customer_collection = []
    for i in range(customers):
        customer_collection.append(customer_record())


    #-------------------------------------------
    # Create Product Reviews

    # Read in fake latin phrase as a list of words
    with open("lorem_ipsum.csv") as my_file:
        random_words = my_file.read().splitlines()
    for i in range(len(random_words)):
        random_words[i] = re.sub(r".*,", "", random_words[i]).lower()
    random_words = random_words[1:]

    # Define a function to generate fake sentences
    def random_sentences(count=1):
        def sentence():
            my_sentence = ""
            for i in range(np.random.randint(10, 20)):
                my_sentence += np.random.choice(random_words, replace=False).lower()+" "
            return my_sentence[0].upper()+my_sentence[1:-1]+"."
        if count==1:
            return sentence()
        else:
            many_sentences = ""
            while count > 0:
                many_sentences += " "+sentence()
                count += -1
            return many_sentences[1:]


    # Create a function to generate customer_review entries
    def customer_review():
        return {"customer_id": np.random.choice(customer_collection)["cust_id"], 
                "rating": np.random.randint(0,10)*0.5, 
                "review": random_sentences(np.random.randint(1,4))}


    #-----------------------------------------------
    # Create product_collection and export it as a json file

    # ---Function begin---
    def product_record():
        bar_types = ["Chocolate Bar", "Candy Bar"]
        centers = ["soft", "fruit", "nut and chews", "chocolate and caramel", "chocolate and walnuts"]
        chocolate_types = ["milk chocolate", "dark chocolate", "white chocolate", "assorted chocolate"]
        dietaries = ["kosher", "egg free", "nut free", "sugar free"]
        fillings = ["caramel", "milk chocolate ganache", "dark chocolate ganache", "marshmallow", "creme"]

        center_type = field_decider(centers, prob = 0.35)
        chocolate_type = field_decider(chocolate_types)
        dietary = field_decider(dietaries, prob = 0.2)
        bar_type = field_decider(bar_types, prob=0.2)
        filling_type = field_decider(fillings, prob=0.33)

        qualities = [center_type, chocolate_type, dietary, bar_type, filling_type]
        qualities = list(filter(lambda i: i != "None", qualities))

        _record = {}

        _record["product_id"]=hex_key(6)
        _record["weight"] = str(np.random.randint(1, 25))+" oz"
        _record["count"] = np.random.choice([1, np.random.randint(1, 25)])
        _record["cost"] = 0.25*np.random.randint(4, 200)
        _record["center_type"] = center_type
        _record["chocolate_type"] = chocolate_type
        _record["dietary"] = dietary
        _record["bar_type"] = bar_type
        _record["filling_type"] = filling_type
        _record["qoh"] = np.random.randint(0, 500)
        _record["reorder_indicator"] = np.random.choice([0, 1], p=(0.05, 0.95))

        reviews = []
        for i in range(np.random.randint(0, 10)):
            reviews.append(customer_review())

        _record['reviews'] = reviews


        def candy_name_generator():
            desc_start = ["mini", "gold", "cinnamon", "birthday", "butterscotch", "scotchmallow", 
                          "assorted", "lollypop", "double", "maple", "triple", "sour"]
            desc_end = ["balls", "twists", "krispys", "bar", "brittle", "square", "JackOLanterns", 
                        "bundle", "bats", "leaves"]
            candy_name = ""
            if len(qualities)>1:
                middle_1, middle_2 = qualities[0], qualities[1]
                candy_name = np.random.choice(desc_start)+" "+middle_1+" "+middle_2+" "+np.random.choice(desc_end)
            elif len(qualities)>0:
                middle = qualities[0]
                candy_name = np.random.choice(desc_start)+" "+middle+" "+np.random.choice(desc_end)          
            else:
                candy_name = np.random.choice(desc_start)+" "+np.random.choice(desc_end)
            return candy_name


        _record["product_name"] = candy_name_generator().title()
        return _record
    # ---Function end---


    # create the product documents and add them to the collection
    product_collection = []
    for i in range(products):
        product_collection.append(product_record())

    # export the completed product documents as a json file
    with open(r'product_collection.json', 'w') as file:
        file.write(str(product_collection).replace("\'", "\""))


    #-------------------------------------------
    # Generate an order

    # Generate Promo code list required for order details
    order_date = date.today()

    def generate_promo():
        _promo = {}
        _promo["code"] = hex_key(12)
        _promo["discount"] = round(np.random.uniform(low=.05, high=.50), 2)
        return _promo

    promo_list =[]

    for i in range(20):
        promo_list.append(generate_promo())


    # create a function that adds valid dates to the promo
    def append_promo_dates(data= np.random.choice(promo_list), init_date=order_date):
        start_date = init_date - timedelta(days=np.random.randint(0, company_age))
        data["start_date"] = start_date
        data["end_date"] = init_date +timedelta(days=np.random.randint(0, 60))
        return data


    # Generate Order Item entries
    def order_items(docs=product_collection):
        def weighted_number():
            number_list = np.arange(1, 11, 1)
            probs = probs = (0.5, 0.18, 0.13, 0.06, 0.04, 0.03, 0.02, 0.02, 0.01, 0.01)
            return np.random.choice(number_list, p=probs)

        products_ordered = np.random.choice(docs, size=weighted_number(), replace=False)
        _order_items = []

        for product in products_ordered: 
            _product_ordered = {}
            _product_ordered["product_name"] = product["product_name"]
            _product_ordered["price"] = product["cost"]
            _product_ordered["count"] = weighted_number()
            _order_items.append(_product_ordered)

        return _order_items


    # Create an order
    def random_order(customer_record):
        acct_created = customer_record["acct_created"]
        ship_to = np.random.choice(customer_record["shipping_addresses"])
        valid_day_delta = days_between(acct_created, date.today())
        order_date = acct_created + timedelta(days = np.random.randint(0, valid_day_delta))

        _order = {}

        _order["order_id"] = hex_key(10)
        _order["order_date"] = order_date
        _order["order_items"] = order_items()
        _order["address_id"] = ship_to["address_id"]
        _order["shipping_cost"] = round(np.random.uniform(low=0, high=50), 2)

        promo = field_decider(promo_list, 0.25)
        if promo != "None":
            promo = append_promo_dates(data=promo)
        _order["promotion"] = promo

        return _order


    # -------------------------------------------
    # Complete customer_collection by adding orders to customer documents
    # and then export the collection as a json file
    order_ct = np.arange(0, 10, 1)
    order_ct_probs = (0.05, 0.4, 0.2, 0.1, 0.05, 0.05, 0.05, 0.05, 0.025, 0.025)

    for document in customer_collection:
        i = np.random.choice(order_ct, p=order_ct_probs)
        document["order"] = []
        while i > 0:
            document["order"].append(random_order(document))
            i += -1

    # Alter Date syntax for JSON interpretability. Replace " ' " w/ " " ".
    
    cc_str = str(customer_collection).replace('\'', "\"")
    
    # dates are not represented in ISO format and are missing 0's for months/days with
    # single digits. We'll execute multiple regular expressions to fix this
    
   
    regex_1 = r"datetime.date.(?P<year>[\d]{4})\, (?P<month>[\d])\, (?P<day>[\d][\d])."
    cc_str = re.sub(regex_1, r'{"$date": "\g<year>-0\g<month>-\g<day>T00:00:00Z"}', cc_str)
    regex_2 = r"datetime.date.(?P<year>[\d]{4})\, (?P<month>[\d][\d])\, (?P<day>[\d])[\D]"
    cc_str = re.sub(regex_2, r'{"$date": "\g<year>-\g<month>-0\g<day>T00:00:00Z"}', cc_str)
    regex_3 = r"datetime.date.(?P<year>[\d]{4})\, (?P<month>[\d])\, (?P<day>[\d])[\D]"
    cc_str = re.sub(regex_3, r'{"$date": "\g<year>-0\g<month>-0\g<day>T00:00:00Z"}', cc_str)
    regex_4 = r"datetime.date.(?P<year>[\d]{4})\, (?P<month>[\d][\d])\, (?P<day>[\d][\d])."
    cc_str = re.sub(regex_4, r'{"$date": "\g<year>-\g<month>-\g<day>T00:00:00Z"}', cc_str)
    
    cc_str = cc_str.replace(")", "")

    with open(r'customer_collection.json', 'w') as file:
        file.write(cc_str)