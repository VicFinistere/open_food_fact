""""
A program to use database data from the API of Openfoodfact
"""
# !/usr/bin/python
# -*- coding: utf-8 -*-
from admin_interface import admin_entry
from client_interface import substitute_product_from_category, list_substitutes
from client_interface import make_a_choice as client_choice


def make_a_choice():
    """
    Actions user can perform
    """
    print("""
`MMMMMMMb.                          MM                                                  
 MM    `Mb                          MM                                                  
 MM     MM ___   ___ ___  __        MM____     ____  ___   ___ ___  __ ___  __   ____   
 MM     MM `MM    MM `MM 6MM        MMMMMMb   6MMMMb `MM    MM `MM 6MM `MM 6MM  6MMMMb  
 MM    .M9  MM    MM  MM69 "        MM'  `Mb 6M'  `Mb MM    MM  MM69 "  MM69 " 6M'  `Mb 
 MMMMMMM9'  MM    MM  MM'           MM    MM MM    MM MM    MM  MM'     MM'    MM    MM 
 MM         MM    MM  MM            MM    MM MMMMMMMM MM    MM  MM      MM     MMMMMMMM 
 MM         MM    MM  MM            MM    MM MM       MM    MM  MM      MM     MM               
 MM         YM.   MM  MM            MM.  ,M9 YM    d9 YM.   MM  MM      MM     YM    d9 
_MM_         YMMM9MM__MM_          _MYMMMM9   YMMMM9   YMMM9MM__MM_    _MM_     YMMMM9      
    """)
    print("Bonjour ! Voulez-vous : ...")
    print("\t", '* "1" => Substituer un aliment en tapant : 1')
    print("\t", '* "2" => Retrouver vos aliments substitués en tapant : 2 ')
    print("\t", '* ou bien accéder à l\'interface d\'administration : "admin"')
    print("\n")
    choice = input("Inscrivez votre choix\t")
    print("Merci !")

    if choice == "1":
        print("Nous allons vous proposer une catégorie de produits. Vous pourrez alors trouver une alternative !")
        substitute_product_from_category()
    elif choice == "2":
        print("Dans un très bref instant vous accéderez à la section dédiée à vos enregistrements de produits...")
        list_substitutes()
    elif choice == "admin":
        print("\n")
        print("Pour procéder à cette option nous vous demandons un mot de passe administrateur.")
        password = input("Entrez le mot de passe s'il vous plaît...\t")
        if password == "******":
            admin_entry()
        else:
            print("Vous ne possédez pas le mot de passe administrateur...")
            print("Le programme va se fermer.")
            client_choice("quit")
    else:
        print("Essayez encore...")
        make_a_choice()


if __name__ == "__main__":
    make_a_choice()
