""""
A program to use database data from the API of Openfoodfact
"""
# !/usr/bin/python
# -*- coding: utf-8 -*-
from connection import Connection
from admin_interface import feed_database
from client_interface import seek_substitutes_products, list_substitutes


def make_a_choice():
    """
    Actions user can perform
    """
    print("\n")
    print("Bonjour ! Voulez-vous 1 = substituer un aliment  ou 2 = retrouver vos aliments substitués ?")
    choice = input("Inscrire le numéro de votre choix")

    if choice == "1":
        seek_substitutes_products()
    elif choice == "2":
        list_substitutes()
    elif choice == "feed database":
        feed_database()
    else:
        print("Essayez encore...")
        make_a_choice()


if __name__ == "__main__":
    make_a_choice()
