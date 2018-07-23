""""
A program to call database where openfoodfact.table contains multiple informations referenced in the README.md
"""
# !/usr/bin/python
# -*- coding: utf-8 -*-
from connection import Connection
import requests
from product import Product
from client_interface import make_a_choice as client_interface
import warnings


def admin_entry(url="https://fr.openfoodfacts.org/"):
    """
    Administrator menu
    :param: url : Open Food Fact URL
    """
    print("\n")
    print("Vous êtes dans l'interface administrateur !")
    print("\t * 1 : Choisir une catégorie de produits à insérer ou mettre à jour dans la base de données")
    print("\t * 2 : Aller dans l'interface utilisateur ")
    print("\n")

    choice = input("Inscrire votre choix\t")
    if choice == "1":
        select_category(url)
    elif choice == "2":
        client_interface("start")


def select_category(url):
    """
    Find a substitute
    """
    print("\n")
    print("A présent dans quelle catégorie voulez-vous ajouter des données ?")
    print("\n")
    print("\t * 1 : sodas à l'orange")
    print("\t * 2 : nems")
    print("\t * 3 : tartelettes")
    print("\t * 4 : sandwichs au fromage")
    print("\t * 5 = pizzas au fromage")
    print("\t * 6 = frites")
    print("\t * 7 = steack hachés surgelés")
    print("\t * 8 = tartes sucrées")
    print("\t * 9 = pâtes à tartiner (noisettes/cacao)")
    short_url = url
    url_filter = "category"
    parameter = ""
    print("\n")
    input_category = input("Entrez un numéro de catégorie s'il vous plaît !\t")
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
            url = [short_url, url_filter, parameter]
            product_count = count_product(url)
            get_products(url, product_count)
        else:
            select_category(url)
    except ValueError:
        select_category(url)


def count_product(url):
    """
    Getting product count from api
    :param url: Page url
    :return: product_count
    """
    short_url, url_filter, parameter = url[0], url[1], url[2]
    print("\n")
    print(f"Récupération du nombre de produits depuis {short_url}/{url_filter}/{parameter}.json...")
    req = requests.get(f"{short_url}/{url_filter}/{parameter}.json")
    json_response = req.json()
    return json_response["count"]


def calculate_parsing_loops(product_count):
    """
    Calculating number of iteration loops to parse all products
    :param product_count:
    :return:
    """
    products_in_page = 20
    amount_last_page_products = 0

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
        amount_last_page_products = listed_amount[-1]

        # Last number is not 0 : we need to get the last products
        if amount_last_page_products != 0:
            if len(listed_amount) > 1:
                if listed_amount[-2] % 2 != 0:
                    amount_last_page_products += 10

    return products_in_page, page_range, amount_last_page_products


def get_products(url, product_count):
    """
    Get products from page
    :param url: Page url
    :param product_count: Number of products
    """
    create_tables()
    products_in_page, page_range, amount_last_page_products = calculate_parsing_loops(product_count)
    page = 0
    short_url, url_filter, parameter = url[0], url[1], url[2]
    for page in range(page_range):
        json_response = request_page(url, page)
        product_dictionary = json_response["products"]
        for product in range(products_in_page):
            get_product_values(product, parameter, product_dictionary)
            product += 1
    get_last_products(amount_last_page_products, url, page)
    admin_entry()


def get_last_products(amount_last_page_products, url, page):
    """
    Get the last page products
    :param amount_last_page_products: amount of last page products
    :param url: URL page
    :param page: Current page
    :return: 1
    """
    short_url, url_filter, parameter = url[0], url[1], url[2]
    if amount_last_page_products != 0:
        print(f"Récupération des {amount_last_page_products} derniers produits "
              f"depuis {short_url}/{url_filter}/{parameter}/{page+1}.json...")
        json_response = request_page(url, page+1)
        product_dictionary = json_response["products"]
        for product in range(amount_last_page_products):
            get_product_values(product, parameter, product_dictionary)
            product += 1


def request_page(url, page):
    """
    :param url: Page url
    :param page: Current page
    :return: Page in json format
    """
    # Get the page
    print("\n")
    short_url, url_filter, parameter = url[0], url[1], url[2]
    print(f"Récupération des produits depuis {short_url}/{url_filter}/{parameter}/{page+1}.json ...")
    req = requests.get(f"{short_url}/{url_filter}/{parameter}/{page+1}.json")
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
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        connection = Connection.connect_to_database()
        cursor = connection.cursor()
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
