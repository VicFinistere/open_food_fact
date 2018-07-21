""""
The static class to handle product categories when feeding database
"""
# !/usr/bin/python
# -*- coding: utf-8 -*-
from connection import Connection


class Category:
    """
    Class to handle categories
    """

    @staticmethod
    def save_category(category):
        """
        Save category if it doesn't appear in database table categories
        """

        # Check if the category is already in table
        connection, cursor = Connection.connect_to_database()
        cursor.execute(f"SELECT COUNT(*) AS category_counter FROM openfoodfact.categories "
                       f"WHERE Name = '{category}'")
        cursor.close()
        connection.close()
        # Get the answer
        check_category = cursor.fetchone()

        # If the category is not already in database table
        if check_category[0] == 0:
            # Insert in table
            connection, cursor = Connection.connect_to_database()
            cursor.execute(f"INSERT INTO openfoodfact.categories(name) VALUES ('{category}')")

            # Commit
            connection.commit()
            cursor.close()
            connection.close()