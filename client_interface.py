""""
A program to use database data from the API of Openfoodfact
"""
# !/usr/bin/python
# -*- coding: utf-8 -*-
from connection import Connection
import warnings


def make_a_choice(choice="start"):
    """
    Actions user can perform
    """
    print("\n")
    if choice == "start":
        print("Voulez-vous 1 = substituer un aliment  ou 2 = retrouver vos aliments substitués ? ")
        print("(Pour quitter inscrire 'quit' )")
        choice = input("Inscrire votre choix\t")

        if choice == "1":
            substitute_product_from_category()
        elif choice == "2":
            list_substitutes()
        elif choice == "quit":
            make_a_choice("quit")
        else:
            print("Essayez encore...")
            make_a_choice("start")

    elif choice == "quit":
        print("")
        print("""          
                           ___                            
                          //\/\   (q\_/p)               ______________    
                          \/\//    /. .\/            --(  'Au revoir' ) 
                          (||_____=\_t_/=   __          --------------
                          ( ||------    \   (                  
                           ||     (    ))   )
                           ||     /   (/\  /
                           ||     \  Y  /-'
                           --      nn^nn                                           
        """)
        exit(0)


def get_categories():
    """
    Getting the categories from database
    :return: categories
    """
    connection = Connection.connect_to_database()
    cursor = connection.cursor()
    get_categories_req = f"SELECT name FROM openfoodfact.categories"
    cursor.execute(get_categories_req)
    categories = cursor.fetchall()
    cursor.close()
    connection.close()
    return categories


def list_substitutes():
    """
    List substitutes from database substitution table
    """
    connection = Connection.connect_to_database()
    cursor = connection.cursor()
    get_substitutes_req = f"SELECT * FROM openfoodfact.substitution"
    cursor.execute(get_substitutes_req)
    substitutes = cursor.fetchall()
    cursor.close()
    connection.close()
    show_substitutes(substitutes)


def show_substitutes(substitutes):
    """
    Show substitution table rows
    :param substitutes: All results from substitution table
    """
    substitution_amount = len(substitutes)
    if substitution_amount == 0:
        print("\n")
        print("\n")
        print("Vous n'avez pas de sauvegardes de produits substitués !")
        print("\n")
        print("Retour à l'interface utilisateur...")
        make_a_choice("start")
    else:
        for substitution_row in range(substitution_amount):
            # Get all substituted products
            show_substituted_product_req = f"SELECT * FROM openfoodfact.products " \
                                           f"WHERE id = {substitutes[substitution_row][0]}"

            connection = Connection.connect_to_database()
            cursor = connection.cursor()
            cursor.execute(show_substituted_product_req)
            substituted = cursor.fetchall()
            cursor.close()
            connection.close()
            print("\n")
            print(f"Vous avez trouvé un substitut pour le {substituted[0][1]}")
            print(substituted[0][1], substituted[0][2], substituted[0][3])

            # Get all substitutes products
            connection = Connection.connect_to_database()
            cursor = connection.cursor()
            show_substitute_product_req = f"SELECT * FROM openfoodfact.products " \
                                          f"WHERE id = {substitutes[substitution_row][1]}"
            cursor.execute(show_substitute_product_req)
            substitute = cursor.fetchall()
            cursor.close()
            connection.close()
            print("\n")
            print(f" Il s'agit de {substitute[0][1]}")
            print(substitute[0][1], substitute[0][2], substitute[0][3])
            truncate_req = input("Voulez vous vider cette liste ? (Y/N)\t")
            if truncate_req == "Y" or truncate_req == "y":
                truncate_substitution_table()
                make_a_choice("quit")
            else:
                make_a_choice("start")

        if substitution_amount == 0:
            print("Il n'y a plus de produits dans la liste ...")

        make_a_choice("quit")


def substitute_product_from_category():
    """
    Find a category for product to substitute
    """
    print("\n")
    print("Dans quelle catégorie voulez-vous substituer l'aliment ?")
    categories = get_categories()
    print("\n")
    for category in range(len(categories)):
        print(f"\t * {category+1} : {categories[category][0]}")

    print("\n")
    input_category = input("Entrez un numéro de catégorie\t")
    try:
        category = int(input_category)
        parameter = 0
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
            category_id = select_category_id(parameter)
            products_count = count_products_from_category(category_id)
            get_page_products(products_count, parameter, category_id)
        else:
            print("Entrez un numéro entre 1 et 9 !")
            substitute_product_from_category()
    except ValueError:
        print("Entrez un chiffre !")
        substitute_product_from_category()


def select_category_id(category):
    """
    Find the id of selected category
    :param category: Selected category
    :return: The id of category
    """
    # Seek category request
    if category is None:
        substitute_product_from_category()
    else:
        seek_category_req = f"SELECT id_category FROM openfoodfact.categories WHERE name = '{category}'"
        connection = Connection.connect_to_database()
        cursor = connection.cursor()
        cursor.execute(seek_category_req)
        category_id = cursor.fetchone()
        cursor.close()
        connection.close()
        category_id = category_id[0]
        return category_id


def count_products_from_category(category_id):
    """
    Count the number of product to calculate loops of printing values
    :param category_id: id of the category
    :return: products count
    """
    # Count products from specific category
    count_products_req = f"SELECT COUNT(name) as PRODUCT_COUNTER FROM openfoodfact.products " \
                         f"WHERE id_category = '{category_id}'"
    connection = Connection.connect_to_database()
    cursor = connection.cursor()
    cursor.execute(count_products_req)
    products_count = cursor.fetchone()
    cursor.close()
    connection.close()
    products_count = products_count[0]
    return products_count


def get_page_products(products_count, category_name, category_id):
    """
    Ask the user if he want the previous or the next products
    :param products_count: number of products
    :param category_name: name of the category
    :param category_id: id of the category
    :return:
    """
    # There will be 10 products by page
    product_number = -10
    print(f"Vous avez sélectionné la catégorie {category_name} ")
    for page in range(products_count // 10):
        if product_number >= 10:
            print("\n")
            choice = input("Touche 'n' : Touche 'n' : produits suivants  / Touche 'p': produits précédents\t")
        if product_number == -10:
            print("\n")
            choice = input("Touche 'n' : Afficher les produits\t")
        if choice == "n" or choice == "N":
            product_number += 10
        elif choice == "p" or choice == "P" and product_number >= 10:
            product_number -= 10
        else:
            print("\n")
            print("Ce n'est pas une option !...")
            choice = input("Voulez-vous redémarrer le programme ?(Y/N)\t")
            if choice == "y" or choice == "Y":
                make_a_choice("start")
            else:
                get_page_products(products_count, category_name, category_id)
        get_products(product_number, category_name, category_id)
        ask_to_substitute(product_number, category_id)
        page += 1
    make_a_choice("quit")


def get_products(product_number, category_name, category_id):
    """
    Get products in a list of 10 results
    :param product_number: The current first product in list
    :param category_name: Name of the category
    :param category_id: Id of the category
    :param category_id: The category of products to parse
    """
    for products in range(10):
        parse_product(product_number, category_name, category_id)
        product_number += 1


def parse_product(product_number, category_name, category_id):
    """
    Get the product values
    :param product_number: Current product to parse
    :param category name of the category
    :param category_id: Current category id for product to parse
    """
    seek_category_products = f"SELECT name FROM openfoodfact.products " \
                             f"WHERE id_category = {category_id} LIMIT {product_number}, 1"
    connection = Connection.connect_to_database()
    cursor = connection.cursor()
    cursor.execute(seek_category_products)
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    if len(products[0][0]) == 0:
        name = f"{category_name}"
    else:
        name = products[0][0]
    print(product_number, ":", name)


def ask_to_substitute(first_product_in_list, category_id):
    """
    Ask if the user want to substitute current products
    :param first_product_in_list: the first product in a list of 10
    :param category_id: Current category id
    """
    print("\n")
    choice = input("Voulez vous un substitut à l'un de ces produits ?(Y/N)")
    if choice == "y" or choice == "Y":
        product_number_input = input("Inscrire le numéro...\t")
        product_number = int(product_number_input)
        if first_product_in_list <= product_number <= first_product_in_list + 9:
            selected_product = show_selected_product(product_number, category_id)
            comment_about_grade(selected_product[2])
            find_substitutes(selected_product)
        else:
            print(f"Vous devez saisir une valeur entre {first_product_in_list} et {first_product_in_list+10} ")


def show_selected_product(product_number, category_id):
    """
    Show selected product
    :param product_number: current product
    :param category_id: current category of product
    :return: information about the product
    """
    connection = Connection.connect_to_database()
    cursor = connection.cursor()
    print("\n")
    print(f"Sélection du numéro : {product_number}")
    get_product_req = f"SELECT * FROM openfoodfact.products " \
                      f"WHERE id_category = {category_id} LIMIT {product_number}, 1"
    cursor.execute(get_product_req)
    selected_product = cursor.fetchone()
    cursor.close()
    connection.close()
    print("\n")
    print("name : ", selected_product[1])
    print("nutrition score : ", selected_product[2])
    print("url : ", selected_product[3])
    return selected_product


def comment_about_grade(grade):
    """
    Comment about grade
    :param grade: current product grade
    """
    print("\n")
    if grade == "a":
        print("C'est un excellent produit de grade A ! On va vous en trouver un aussi bien !")
    elif grade == "b":
        print("B ! Ca va être difficile de trouver mieux...Voyons...")
    elif grade == "c":
        print("C...On va trouver mieux !!")
    elif grade == "d":
        print("D ! On va trouver mieux...Vite !")
    else:
        print(f"Le grade est {grade}...Trouvons mieux !!!...")


def find_substitutes(selected_product):
    """
    Find substitute product
    :param selected_product: The product to substitute
    """
    substitute_req = f"SELECT * FROM openfoodfact.products " \
                     f"WHERE id_category = {selected_product[4]} AND grade < '{selected_product[2]}' LIMIT 1"
    connection = Connection.connect_to_database()
    cursor = connection.cursor()
    cursor.execute(substitute_req)
    cursor.close()
    connection.close()
    substitutes = cursor.fetchone()
    if substitutes is None:
        substitute_req = f"SELECT * FROM openfoodfact.products " \
                         f"WHERE id_category = {selected_product[4]} AND grade = '{selected_product[2]}' LIMIT 1"
        connection = Connection.connect_to_database()
        cursor = connection.cursor()
        cursor.execute(substitute_req)
        cursor.close()
        connection.close()
        cursor.close()
        substitutes = cursor.fetchone()
        if selected_product[4] == substitutes[4]:
            print("Il n'y a pas de meilleur nutrition score pour cette catégorie de produit !")

    print("\n")
    print("Substitut : ", substitutes[1])
    print("Grade : ", substitutes[2])
    print("URL : ", substitutes[3])

    print("\n")
    choice = input("Voulez-vous sauvegarder ce substitut ?(Y/N)\t")
    if choice == "y" or choice == "Y":
        save_substitution(selected_product, substitutes)


def save_substitution(selected_product, substitutes):
    """
    Save the substitution
    :param selected_product: The product substituted
    :param substitutes: The substitute
    """
    create_table_substitution()
    inserting_products_id(selected_product[0], substitutes[0])


def create_table_substitution():
    """
    Create table substitution if not exists
    """
    connection = Connection.connect_to_database()
    cursor = connection.cursor()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        cursor.execute("""CREATE TABLE IF NOT EXISTS substitution(
        id_product INTEGER, id_substituted_product INTEGER) """)
    cursor.close()
    connection.close()


def inserting_products_id(product, substitute):
    insertion_req = f"INSERT INTO openfoodfact.substitution(id_product, id_substituted_product) " \
                    f"VALUES ({product},{substitute})"
    connection = Connection.connect_to_database()
    cursor = connection.cursor()
    cursor.execute(insertion_req)
    connection.commit()
    cursor.close()
    connection.close()
    print(
        "Vous pouvez retrouver vos produits substitués en choisissant l'option dédiée au démarrage de l'application !")
    make_a_choice("start")


def truncate_substitution_table():
    """
    Truncate table substitution
    """
    connection = Connection.connect_to_database()
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE openfoodfact.substitution")
    cursor.close()
    connection.close()
