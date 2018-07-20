#!/usr/local/bin/python
from connection import Connection


def make_a_choice():
    print("Hi ! Do you want 1 = to substitute a product  or 2 = to find substituted products ?")
    input_choice = input("Enter the number")

    choice = int(input_choice)
    if choice == 1:
        connection, cursor = Connection.connect_to_database()
        Connection.close_database_connection(cursor, connection)
    elif choice == 2:
        print("You can now find substituted products")
    else:
        print("Please try again...")
        make_a_choice()


if __name__ == "__main__":
    make_a_choice()
