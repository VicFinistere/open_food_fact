#!/usr/local/bin/python

if __name__ == "__main__":
    print("Hi ! Do you want 1 = to substitute a product  or 2 = to find substituted products ?")
    input_choice = input("Enter the number")

    choice = int(input_choice)
    if choice == 1:
        print("You can now substitute a product")
    elif choice == 2:
        print("You can now find substituted products")
