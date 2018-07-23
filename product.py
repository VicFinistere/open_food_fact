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

    def get_id_category(self):
        # Get the id category in table categories where name correspond
        connection = Connection.connect_to_database()
        cursor = connection.cursor()
        cursor.execute(f"SELECT id_category FROM openfoodfact.categories WHERE name = '{self.category}' ")

        # Return the id
        fetch_category_id = cursor.fetchone()
        cursor.close()
        connection.close()
        return fetch_category_id

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
        product_exists = self.check_product_in_table()
        # If the product is not already in database table
        if product_exists[0] == 0:
            fetch_category_id = self.get_id_category()

            # Get only the number in response
            category_id = fetch_category_id[0]
            self.insert_in_products_table(category_id)
            redundant_products = self.check_redundant()
            if redundant_products is not None:
                for redundant_product in range(0, len(redundant_products), 2):
                    redundant_ids = redundant_products[redundant_product]
                    for redundant_id in range(len(redundant_ids)):
                        self.delete_redundant(redundant_ids, redundant_id)

    def insert_in_products_table(self, category_id):
        """
        Insert product in products table
        :param category_id: the id of category
        """
        connection = Connection.connect_to_database()
        cursor = connection.cursor()
        # Insert in table the new product
        cursor.execute(f'INSERT INTO openfoodfact.products(name, grade, url, id_category) '
                       f'VALUES ("{self.name}", "{self.grade}", "{self.url}", {category_id})')

        # Commit
        connection.commit()
        cursor.close()
        connection.close()

    def check_product_in_table(self):
        """
        Check if product exists before insertion
        """
        connection = Connection.connect_to_database()
        cursor = connection.cursor()
        cursor.execute(f"SELECT COUNT(*) AS product_counter FROM openfoodfact.products "
                       f"WHERE Name = '{self.name}'")

        # Get the answer
        product_exists = cursor.fetchone()
        cursor.close()
        connection.close()
        return product_exists

    @staticmethod
    def check_redundant():
        """
        Remove redundant products in products table
        """
        connection = Connection.connect_to_database()
        cursor = connection.cursor()
        cursor.execute(f"SELECT id FROM openfoodfact.products pro1 WHERE EXISTS ("
                       f"SELECT 1 FROM openfoodfact.products pro2 WHERE pro1.name = pro2.name LIMIT 1, 1 )")
        redundant_products = cursor.fetchall()
        cursor.close()
        connection.close()
        return redundant_products

    @staticmethod
    def delete_redundant(redundant_ids, redundant_id):
        """
        Remove redundant products
        :param redundant_ids:
        :param redundant_id:
        """
        connection = Connection.connect_to_database()
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM openfoodfact.products WHERE "
                       f"id = {redundant_ids[redundant_id]} ")
        connection.commit()
        cursor.close()
        connection.close()