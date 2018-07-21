""""
A program to call database where openfoodfact.table contains multiple informations referenced in the README.md
"""
# !/usr/bin/python
# -*- coding: utf-8 -*-
from connection import Connection
import requests
from product import Product


def feed_database(url="https://fr.openfoodfacts.org/"):
    """
    Action user can perform
    """

    choice = input("1 = Alimenter la base de données")
    if choice == "1":
        select_category(url)
    else:
        print("Veuillez réessayer...")
        feed_database(url)


def select_category(url):
    """
    Find a substitute
    """
    print("Dans quelle catégorie voulez-vous ajouter des données ?")
    print("1 = sodas à l'orange,"
          "2 = nems,"
          "3 = tartelettes,"
          "4 = sandwichs au fromage,"
          "5 = pizzas au fromage,"
          "6 = frites,"
          "7 = steaks hachés surgelés,"
          "8 = tartes sucrées,"
          "9 = pates-a-tartiner-aux-noisettes-et-au-cacao")

    url_filter = "category"
    parameter = ""

    input_category = input("Enter un numéro de catégorie")
    try:
        category = int(input_category)
        if category == 1:
            parameter = "sodas-a-l-orange"

        elif category == 2:
            parameter = "nems"

        elif category == 3:
            parameter = "tartelettes"

        elif category == 4:
            parameter = "sandwichs-au-fromage"

        elif category == 5:
            parameter = "pizzas-au-fromage"

        elif category == 6:
            parameter = "frites"

        elif category == 7:
            parameter = "steaks-haches-surgeles"

        elif category == 8:
            parameter = "tartes-sucrees"

        elif category == 9:
            parameter = "pates-a-tartiner-aux-noisettes"

        if 0 < category < 10:
            product_count = count_product(url, url_filter, parameter)
            get_products(url, url_filter, parameter, product_count)
        else:
            select_category(url)
    except ValueError:
        select_category(url)


def count_product(url, url_filter, parameter):
    """
    Getting product count from api
    :param url: Page url
    :param url_filter: Page path access
    :param parameter: Page filter
    :return: product_count
    """
    print(f"Récupération du nombre de produits depuis {url}/{url_filter}/{parameter}.json...")
    req = requests.get(f"{url}/{url_filter}/{parameter}.json")
    json_response = req.json()
    return json_response["count"]


def calculate_parsing_loops(product_count):
    """
    Calculating number of iteration loops to parse all products
    :param product_count:
    :return:
    """
    products_in_page = 20
    amount_last_number = 0

    # if products < 20 : products in page = number of products
    if product_count < products_in_page:
        products_in_page = product_count
        page_range = 1

    # if products > 20 : page range is products // 20
    else:
        page_range = product_count // products_in_page

        # Get the amount of products in a list
        # ( example : [ 2, 1] )
        listed_amount = [int(i) for i in str(product_count)]

        # Get the last items
        # ( example : 1 in the last page)
        amount_last_number = listed_amount[-1]

        # Last number is not 0 : we need to get the last products
        if amount_last_number != 0:
            if len(listed_amount) > 1:
                if listed_amount[-2] % 2 != 0:
                    amount_last_number += 10

    return products_in_page, page_range, amount_last_number


def get_products(url, url_filter, parameter, product_count):
    """
    Get products from page
    :param url: Page url
    :param url_filter: Page path access
    :param parameter: Page filter
    :param product_count: Number of products
    """
    create_tables()
    products_in_page, page_range, amount_last_number = calculate_parsing_loops(product_count)

    for page in range(page_range):

        json_response = request_page(url, url_filter, parameter, page)
        product_dictionary = json_response["products"]
        for product in range(products_in_page):
            get_product_values(product, parameter, product_dictionary)
            product += 1
        page += 1

        if amount_last_number != 0:
            request_page(url, url_filter, parameter, page)
            product_dictionary = json_response["products"]
            for product in range(amount_last_number):
                get_product_values(product, parameter, product_dictionary)
                product += 1


def request_page(url, url_filter, parameter, page):
    """
    :param url: Page url
    :param url_filter: Page path access
    :param parameter: Page filter
    :param page: Current page
    :return: Page in json format
    """
    # Get the page
    print(f"Récupération des produits depuis {url}/{url_filter}/{parameter}/{page+1}.json ...")
    req = requests.get(f"{url}/{url_filter}/{parameter}/{page+1}.json")
    json_response = req.json()
    return json_response


def get_product_values(product, product_category, product_dictionary):
    """
    Get product values
    :param product: Current product
    :param product_category: Current category product
    :param product_dictionary: Current Json Page in json format
    :return:
    """
    product_name, product_grade, product_url = 0, 0, 0
    if "product_name_fr" in product_dictionary[product]:
        product_name = product_dictionary[product]["product_name_fr"]
        product_name = product_name.replace("'", "''")
        print("Name :", product_name)

    if "nutrition_grades" in product_dictionary[product]:
        product_grade = product_dictionary[product]["nutrition_grades"]
        print("Nutrition grade :", product_grade)

    if "url" in product_dictionary[product]:
        product_url = product_dictionary[product]["url"]
        print("URL :", product_url)

    if product_name != 0 and product_category != 0 and product_grade != 0 and product_url != 0:
        product_values = [product_name, product_category, product_grade, product_url]
        new_product = Product(product_values)
        new_product.save()


def create_tables():
    """
    Create tables if not exists
    """
    connection, cursor = Connection.connect_to_database()
    cursor.execute("""CREATE TABLE IF NOT EXISTS categories(
                id_category INTEGER PRIMARY KEY AUTO_INCREMENT UNIQUE, name TEXT) """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY AUTO_INCREMENT UNIQUE, 
                name TEXT,  
                grade VARCHAR(50), 
                url TEXT,
                id_category INTEGER(1),
                FOREIGN KEY fk_category(id_category)
                REFERENCES
                categories(id_category)
                ON UPDATE CASCADE
                ON DELETE RESTRICT) """)
    cursor.close()
    connection.close()
