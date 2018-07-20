#!/usr/local/bin/python
from connection import Connection


def make_a_choice():
    print("Hi ! Do you want 1 = to substitute a product  or 2 = to find substituted products ?")
    input_choice = input("Enter the number")

    choice = int(input_choice)
    if choice == 1:
        category = select_category()
        seek_substitutes_products(category)
    elif choice == 2:
        print("You can now find substituted products")
    else:
        print("Please try again...")
        make_a_choice()


def select_category():
    """
        Find a substitute
        """
    print("Dans quelle catégorie voulez-vous substituer l'aliment ?")
    print("1 = boissons végétales,"
          "2 = eaux minérales naturelles,"
          "3 = tartelettes,"
          "4 = sandwichs au fromage,"
          "5 = pizzas au fromage,"
          "6 = frites,"
          "7 = steaks hachés surgelés,"
          "8 = tartes sucrées,"
          "9 = pates-a-tartiner-aux-noisettes-et-au-cacao")

    input_category = input("Enter un numéro de catégorie")
    try:
        category = int(input_category)
        parameter = 0
        if category == 1:
            parameter = "boissons-vegetales"

        elif category == 2:
            parameter = "eaux-minerales-naturelles"

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
            return parameter
        else:
            select_category()
    except ValueError:
        select_category()


def select_category_id(category):
    # Seek category request
    connection, cursor = Connection.connect_to_database()
    seek_category_req = f"SELECT id_category FROM openfoodfact.categories WHERE name = '{category}'"
    cursor.execute(seek_category_req)
    category_id = cursor.fetchall()
    category_id = category_id[0][0]
    Connection.close_database_connection(cursor, connection)
    return category_id


def count_products_from_category(category_id):
    connection, cursor = Connection.connect_to_database()
    # Count products from specific category
    count_products_req = f"SELECT COUNT(name) as PRODUCT_COUNTER FROM openfoodfact.products " \
                         f"WHERE id_category = '{category_id}'"
    cursor.execute(count_products_req)
    products_count = cursor.fetchone()
    products_count = products_count[0]
    Connection.close_database_connection(cursor, connection)
    input_next_products(products_count, category_id)


def input_next_products(products_count, category_id):
    # There will be 10 products by page
    product_number = -10
    for page in range(products_count // 10):
        if product_number >= 10:
            choice = input("press 'n' to get next products / 'p' to get previous products")
        else:
            choice = input(" press 'n' to get next products")
        if choice == "n" or choice == "N":
            product_number += 10
        elif choice == "p" or choice == "P" and product_number >= 10:
            product_number -= 10
        else:
            print("Try again...")
            input_next_products(products_count, category_id)
        get_products(product_number, category_id)


def get_products(product_number, category_id):
    for products in range(10):
        parse_product(product_number, category_id)
        product_number += 1


def parse_product(product_number, category_id):
    connection, cursor = Connection.connect_to_database()
    seek_category_products = f"SELECT name FROM openfoodfact.products " \
                             f"WHERE id_category = {category_id} LIMIT {product_number}, 1"
    cursor.execute(seek_category_products)
    products = cursor.fetchall()
    print(product_number, ":", products[0][0])
    Connection.close_database_connection(connection, cursor)


def seek_substitutes_products(category):
    # connection, cursor = Connection.connect_to_database()
    category_id = select_category_id(category)
    count_products_from_category(category_id)
    # Connection.close_database_connection(connection, cursor)


if __name__ == "__main__":
    make_a_choice()
