"""Menus for Caesar Cipher, Rail Fence Cipher, and Product Cipher."""

import caesar
import railfence
import product_cipher


def caesar_menu():
    while True:
        print("\n" + "=" * 50)
        print("CAESAR CIPHER - Interactive Menu")
        print("=" * 50)
        print("1. Encrypt text")
        print("2. Decrypt text")
        print("3. Brute force attack")
        print("4. Encrypt file")
        print("5. Decrypt file")
        print("6. Frequency analysis")
        print("7. Cryptanalyze file (Exhaustive Search)")
        print("8. Cryptanalyze file (Frequency Analysis)")
        print("0. Back to main menu")
        print("-" * 50)

        choice = input("Enter your choice (0-8): ").strip()

        if choice == "1":
            plaintext = input("Enter plaintext: ")
            key = int(input("Enter key (0-25): "))
            print(f"\nCiphertext: {caesar.encrypt(plaintext, key)}\n")

        elif choice == "2":
            ciphertext = input("Enter ciphertext: ")
            key = int(input("Enter key (0-25): "))
            print(f"\nPlaintext: {caesar.decrypt(ciphertext, key)}\n")

        elif choice == "3":
            ciphertext = input("Enter ciphertext: ")
            print("\nBrute Force Results:")
            caesar.brute_force_exhaustive_display(ciphertext)

        elif choice == "4":
            input_file = input("Enter input file path: ").strip()
            output_file = input("Enter output file path: ").strip()
            key = int(input("Enter key (0-25): "))
            caesar.encrypt_file(input_file, output_file, key)

        elif choice == "5":
            input_file = input("Enter input file path: ").strip()
            output_file = input("Enter output file path: ").strip()
            key = int(input("Enter key (0-25): "))
            caesar.decrypt_file(input_file, output_file, key)

        elif choice == "6":
            ciphertext = input("Enter ciphertext for frequency analysis: ")
            caesar.brute_force_frequency_analysis_display(ciphertext, show_top=5)

        elif choice == "7":
            input_file = input("Enter encrypted file path: ").strip()
            output_file = input("Enter result file path: ").strip()
            caesar.cryptanalyze_file_exhaustive(input_file, output_file)

        elif choice == "8":
            input_file = input("Enter encrypted file path: ").strip()
            output_file = input("Enter result file path: ").strip()
            top_n = int(input("Enter top N candidates (default 5): ") or "5")
            caesar.cryptanalyze_file_frequency(input_file, output_file, top_n)

        elif choice == "0":
            break

        else:
            print("Invalid choice! Please try again.")


def railfence_menu():
    rf_sys = railfence.RailFenceSystem()

    while True:
        print("\n" + "=" * 50)
        print("RAIL FENCE CIPHER - Interactive Menu")
        print("=" * 50)
        print("1. Encrypt text")
        print("2. Decrypt text (Known Key)")
        print("3. Smart Cryptanalysis")
        print("4. Encrypt file")
        print("5. Decrypt file")
        print("6. Cryptanalyze file")
        print("0. Back to main menu")
        print("-" * 50)

        choice = input("Enter your choice (0-6): ").strip()

        if choice == "1":
            plaintext = input("Enter plaintext: ")
            key = int(input("Enter key: "))
            print(f"\nCiphertext: {railfence.encrypt_railfence(plaintext, key)}\n")

        elif choice == "2":
            ciphertext = input("Enter ciphertext: ")
            key = int(input("Enter key: "))
            print(f"\nDecrypted: {railfence.decrypt_railfence(ciphertext, key)}\n")

        elif choice == "3":
            ciphertext = input("Enter ciphertext for analysis: ")
            rf_sys.railfence_cryptanalyze(ciphertext)

        elif choice == "4":
            in_f = input("Enter input file path: ").strip()
            out_f = input("Enter output file path: ").strip()
            key = int(input("Enter key: "))
            railfence.encrypt_file(in_f, out_f, key)

        elif choice == "5":
            in_f = input("Enter input file path: ").strip()
            out_f = input("Enter output file path: ").strip()
            key = int(input("Enter key: "))
            railfence.decrypt_file(in_f, out_f, key)

        elif choice == "6":
            in_f = input("Enter encrypted file path: ").strip()
            out_f = input("Enter result file path: ").strip()
            railfence.cryptanalyze_file(in_f, out_f)

        elif choice == "0":
            break

        else:
            print("Invalid choice! Please try again.")


def product_menu():
    pc_sys = product_cipher.ProductCipherSystem()

    while True:
        print("\n" + "=" * 50)
        print("PRODUCT CIPHER - Interactive Menu")
        print("=" * 50)
        print("1. Encrypt text")
        print("2. Decrypt text (Known Keys)")
        print("3. Smart Cryptanalysis")
        print("4. Encrypt file")
        print("5. Decrypt file")
        print("6. Cryptanalyze file")
        print("0. Back to main menu")
        print("-" * 50)

        choice = input("Enter your choice (0-6): ").strip()

        if choice == "1":
            plaintext = input("Enter plaintext: ")
            caesar_key = int(input("Enter Caesar key (0-25): "))
            rail_key = int(input("Enter Rail Fence key: "))
            ciphertext = product_cipher.encrypt_product(plaintext, caesar_key, rail_key)
            print(f"\nCiphertext: {ciphertext}\n")

        elif choice == "2":
            ciphertext = input("Enter ciphertext: ")
            caesar_key = int(input("Enter Caesar key (0-25): "))
            rail_key = int(input("Enter Rail Fence key: "))
            plaintext = product_cipher.decrypt_product(ciphertext, caesar_key, rail_key)
            print(f"\nDecrypted: {plaintext}\n")

        elif choice == "3":
            ciphertext = input("Enter ciphertext for analysis: ")
            max_rail_key = int(input("Enter max Rail Fence key to test (default 20): ") or "20")
            product_cipher.cryptanalyze_product_display(
                ciphertext,
                max_rail_key=max_rail_key,
                top_n=5,
            )
            pc_sys.product_cryptanalyze(
                ciphertext,
                max_rail_key=max_rail_key,
                top_n=5,
            )

        elif choice == "4":
            input_file = input("Enter input file path: ").strip()
            output_file = input("Enter output file path: ").strip()
            caesar_key = int(input("Enter Caesar key (0-25): "))
            rail_key = int(input("Enter Rail Fence key: "))
            product_cipher.encrypt_file(input_file, output_file, caesar_key, rail_key)

        elif choice == "5":
            input_file = input("Enter input file path: ").strip()
            output_file = input("Enter output file path: ").strip()
            caesar_key = int(input("Enter Caesar key (0-25): "))
            rail_key = int(input("Enter Rail Fence key: "))
            product_cipher.decrypt_file(input_file, output_file, caesar_key, rail_key)

        elif choice == "6":
            input_file = input("Enter encrypted file path: ").strip()
            output_file = input("Enter result file path: ").strip()
            max_rail_key = int(input("Enter max Rail Fence key to test (default 20): ") or "20")
            product_cipher.cryptanalyze_file(
                input_file,
                output_file,
                max_rail_key=max_rail_key,
                top_n=5,
            )

        elif choice == "0":
            break

        else:
            print("Invalid choice! Please try again.")