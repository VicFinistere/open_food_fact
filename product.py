""""
The class to handle products when feeding database
"""
# !/usr/bin/python
# -*- coding: utf-8 -*-
from connection import Connection
from category import Category


class Product:
    """
    Class to handle products
    """

    def __init__(self, product_values):
        self.name = product_values[0]
        self.category = product_values[1]
        self.grade = product_values[2]
        self.url = product_values[3]
        print(product_values)

    def save(self):
        """
        Save the product in database
        """
        Category.save_category(self.category)
        self.save_product()

    def save_product(self):
        """
        Save product if it doesn't appear in database table products
        """
        # Check if the product is already in table
        connection, cursor = Connection.connect_to_database()
        cursor.execute(f"SELECT COUNT(*) AS product_counter FROM openfoodfact.products "
                       f"WHERE Name = '{self.name}'")

        # Get the answer
        check_product = cursor.fetchone()
        cursor.close()
        connection.close()
        # If the product is not already in database table
        if check_product[0] == 0:
            # Get the id category in table categories where name correspond
            connection, cursor = Connection.connect_to_database()
            cursor.execute(f"SELECT id_category FROM openfoodfact.categories WHERE name = '{self.category}' ")

            # Return the id
            fetch_category_id = cursor.fetchone()

            # Get only the number in response
            category_id = fetch_category_id[0]

            # Insert in table the new product
            cursor.execute(f'INSERT INTO openfoodfact.products(name, grade, url, id_category) '
                           f'VALUES ("{self.name}", "{self.grade}", "{self.url}", {category_id})')

            # Commit
            connection.commit()
            cursor.close()
            connection.close()
