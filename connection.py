""""
The static class for connection methods
"""
# !/usr/bin/python
# -*- coding: utf-8 -*-
import pymysql


class Connection:
    """
    Class to create MySQL connection
    """

    @staticmethod
    def connect_to_database():
        """
        Connect to database
        :return: connection to database
        """
        connection = pymysql.connect(host="127.0.0.1",  # The Host
                                     user="root",  # username
                                     passwd="******",  # password
                                     db="openfoodfact",
                                     port=3306)  # name of the data base
        # print("Connexion")
        return connection
