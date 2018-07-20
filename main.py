#!/usr/local/bin/python
from connection import Connection


def make_a_choice():
    print("Hi ! Do you want 1 = to substitute a product  or 2 = to find substituted products ?")
    input_choice = input("Enter the number")

    choice = int(input_choice)
    if choice == 1:
        connection, cursor = Connection.connect_to_database()
        select_category()
        Connection.close_database_connection(cursor, connection)
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
            print(f"Vous avez choisi la catégorie {parameter}")
        else:
            select_category()
    except ValueError:
        select_category()


if __name__ == "__main__":
    make_a_choice()
