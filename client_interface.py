""""
A program to use database data from the API of Openfoodfact
"""
# !/usr/bin/python
# -*- coding: utf-8 -*-
import warnings
from connection import Connection


def client_interface(choice="start"):
    """
    Actions user can perform
    """
    print("\n")
    if choice == "start":
        print("Voulez-vous 1 = substituer un aliment  ou 2 = retrouver vos aliments substitués ? ")
        print("(Pour quitter inscrire 'quit' )")
        choice = input("Inscrire votre choix\t")

        if choice == "1":
            choose_category()
        elif choice == "2":
            list_substitutes()
        elif choice == "quit":
            client_interface("quit")
        else:
            print("Essayez encore...")
            client_interface("start")

    elif choice == "quit":
        print("")
        print(r"""          
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


def choose_category():
    """
    Find a category for product to substitute
    """
    print("\n")
    print("Dans quelle catégorie voulez-vous substituer l'aliment ?")
    categories = get_categories()
    print("\n")
    for number, _ in enumerate(categories):
        print(f"\t * {number+1} : {categories[number][0]}")

    print("\n")
    input_category = input("Entrez un numéro de catégorie\t")
    try:
        category_number = int(input_category)
        if 0 < category_number < 10:
            parameter = categories[category_number][0]
            category_id = select_category_id(parameter)
            products_count = count_products_from_category(category_id)
            get_page_products(products_count, parameter, category_id)
        else:
            print("Entrez un numéro entre 1 et 9 !")
            choose_category()
    except ValueError:
        print("Entrez un chiffre !")
        choose_category()


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


def select_category_id(category):
    """
    Find the id of selected category
    :param category: Selected category
    :return: The id of category
    """
    # Seek category request
    seek_category_req = f"SELECT id_category FROM openfoodfact.categories WHERE name = '{category}'"
    connection = Connection.connect_to_database()
    cursor = connection.cursor()
    cursor.execute(seek_category_req)
    category_id = cursor.fetchone()
    cursor.close()
    connection.close()
    category_id = category_id[0]
    return category_id


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
        choice = ''
        if product_number >= 10:
            print("\n")
            choice = input("Touche 'n' : Touche 'n' : produits suivants  / Touche 'p': produits précédents\t")
        if product_number == -10:
            print("\n")
            choice = input("Touche 'n' : Afficher les produits\t")
        if choice in ('n', 'N'):
            product_number += 10
        elif choice in ('p', 'P') and product_number >= 10:
            product_number -= 10
        else:
            print("\n")
            print("Ce n'est pas une option !...")
            choice = input("Voulez-vous revenir au menu principal ?(Y/N)\t")
            if choice in ('y', 'Y'):
                client_interface("start")
            else:
                get_page_products(products_count, category_name, category_id)
        get_products(product_number, category_name, category_id)
        ask_to_substitute(product_number, category_id)
        page += 1
    client_interface("quit")


def get_products(product_number, category_name, category_id):
    """
    Get products in a list of 10 results
    :param product_number: The current first product in list
    :param category_name: Name of the category
    :param category_id: Id of the category
    :param category_id: The category of products to parse
    """
    for _ in range(10):
        parse_product(product_number, category_name, category_id)
        product_number += 1


def parse_product(product_number, category_name, category_id):
    """
    Get the product values
    :param product_number: Current product to parse
    :param category_name: name of the category
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
    if not products[0][0]:
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
    if choice in ('y', 'Y'):
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
    if choice in ('y', 'Y'):
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
    """
    Insertion of ids in substitution table
    :param product: The id of product substituted
    :param substitute: The id of substitute product
    """
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
    client_interface("start")


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
    page_substitutions(substitutes)


def page_substitutions(substitutes):
    """
    Show substitution table rows
    :param substitutes: All results from substitution table
    """

    if not substitutes:
        print("\n")
        print("\n")
        print("Vous n'avez pas de sauvegardes de produits substitués !")
        print("\n")
        print("Retour à l'interface utilisateur...")
        client_interface("start")
    else:
        for substitution_number, _ in enumerate(substitutes):
            if substitution_number > 0:
                get_other_substitute = input(f"Afficher le produit #{(len(substitutes)-substitution_number)+1} ? (Y/N)")
                if get_other_substitute in ('y', 'Y'):
                    show_substitute(substitutes, substitution_number)
            else:
                show_substitute(substitutes, substitution_number)

        manage_substitution_table()
        if len(substitutes) == 0:
            print("Il n'y a plus de produits dans la liste ...")

        client_interface("quit")


def list_current_substitute(substituted, substitute):
    """
    List substitution current row
    :param substituted:
    :param substitute:
    """
    print("\n")
    print(f"Vous avez trouvé un substitut pour le {substituted[0][1]}")
    print(substituted[0][1], substituted[0][2], substituted[0][3])
    print("\n")
    print(f" Il s'agit de {substitute[0][1]}")
    print(substitute[0][1], substitute[0][2], substitute[0][3])


def show_substitute(substitutes, substitution_number):
    """
    Show current substitution table row
    :param substitutes:
    :param substitution_number:
    :return:
    """
    substituted = get_substituted_product(substitutes, substitution_number)
    substitute = get_substitute_product(substitutes, substitution_number)
    list_current_substitute(substituted, substitute)


def get_substituted_product(substitutes, substitution_row):
    """
    Getting substituted products
    :param substitutes: list of substituted products
    :param substitution_row: current substituted product
    :return: the substituted product
    """
    # Get all substituted products
    show_substituted_product_req = f"SELECT * FROM openfoodfact.products " \
                                   f"WHERE id = {substitutes[substitution_row][0]}"

    connection = Connection.connect_to_database()
    cursor = connection.cursor()
    cursor.execute(show_substituted_product_req)
    substituted = cursor.fetchall()
    cursor.close()
    connection.close()
    return substituted


def get_substitute_product(substitutes, substitution_row):
    """
    Get substitute product
    :param substitutes: list of substitute products
    :param substitution_row: current substitute product
    :return: the substitute product
    """
    connection = Connection.connect_to_database()
    cursor = connection.cursor()
    show_substitute_product_req = f"SELECT * FROM openfoodfact.products " \
                                  f"WHERE id = {substitutes[substitution_row][1]}"
    cursor.execute(show_substitute_product_req)
    substitute = cursor.fetchall()
    cursor.close()
    connection.close()
    return substitute


def manage_substitution_table():
    """
    Manage substitution table
    """
    print("\n")
    truncate_req = input("Voulez vous vider cette liste ? (Y/N)\t")
    if truncate_req in ('y', 'Y'):
        truncate_substitution_table()
        print("La liste de vos substituts alimentaires effacée !")
        client_interface("start")
    else:
        print("Vos substituts alimentaires sont sauvegardées !")
        client_interface("start")


def truncate_substitution_table():
    """
    Truncate table substitution
    """
    connection = Connection.connect_to_database()
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE openfoodfact.substitution")
    cursor.close()
    connection.close()
