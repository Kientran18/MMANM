"""Main program entry point."""

from menu import caesar_menu, railfence_menu, product_menu


def main():
    print("\n" + "=" * 50)
    print("CRYPTOGRAPHY ALGORITHMS - H252")
    print("=" * 50)

    while True:
        print("\nMain Menu:")
        print("1. Caesar Cipher")
        print("2. Rail Fence Cipher")
        print("3. Product Cipher (Caesar + Rail Fence)")
        print("0. Exit")
        print("-" * 50)

        choice = input("Select cipher (0-3): ").strip()

        if choice == "1":
            caesar_menu()
        elif choice == "2":
            railfence_menu()
        elif choice == "3":
            product_menu()
        elif choice == "0":
            print("Thank you for using the program!")
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()