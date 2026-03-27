"""
Main program for Caesar Cipher, Rail Fence, and Product Cipher demonstrations
"""

import caesar
import os
import sys


def caesar_menu():
    """Interactive menu for Caesar Cipher operations"""
    while True:
        print("\n" + "="*50)
        print("CAESAR CIPHER - Interactive Menu")
        print("="*50)
        print("1. Encrypt text")
        print("2. Decrypt text")
        print("3. Brute force attack")
        print("4. Encrypt file")
        print("5. Decrypt file")
        print("6. Frequency analysis")
        print("0. Back to main menu")
        print("-"*50)
        
        choice = input("Enter your choice (0-6): ").strip()
        
        if choice == '1':
            plaintext = input("Enter plaintext: ")
            key = int(input("Enter key (0-25): "))
            ciphertext = caesar.encrypt(plaintext, key)
            print(f"\nCiphertext: {ciphertext}\n")
        
        elif choice == '2':
            ciphertext = input("Enter ciphertext: ")
            key = int(input("Enter key (0-25): "))
            plaintext = caesar.decrypt(ciphertext, key)
            print(f"\nPlaintext: {plaintext}\n")
        
        elif choice == '3':
            ciphertext = input("Enter ciphertext: ")
            print("\nBrute Force Results:")
            caesar.brute_force_display(ciphertext)
        
        elif choice == '4':
            input_file = input("Enter input file path: ").strip()
            output_file = input("Enter output file path: ").strip()
            key = int(input("Enter key (0-25): "))
            caesar.encrypt_file(input_file, output_file, key)
        
        elif choice == '5':
            input_file = input("Enter input file path: ").strip()
            output_file = input("Enter output file path: ").strip()
            key = int(input("Enter key (0-25): "))
            caesar.decrypt_file(input_file, output_file, key)
        
        elif choice == '6':
            text = input("Enter text for frequency analysis: ")
            freq = caesar.analyze_frequency(text)
            caesar.print_frequency(freq)
        
        elif choice == '0':
            break
        
        else:
            print("Invalid choice! Please try again.")


def main():
    """Main program entry point"""
    print("\n" + "="*50)
    print("CRYPTOGRAPHY ALGORITHMS - H252")
    print("="*50)
    
    while True:
        print("\nMain Menu:")
        print("1. Caesar Cipher")
        print("2. Rail Fence Cipher")
        print("3. Product Cipher")
        print("0. Exit")
        print("-"*50)
        
        choice = input("Select cipher (0-3): ").strip()
        
        if choice == '1':
            caesar_menu()
        elif choice == '2':
            print("Rail Fence Cipher - Not yet implemented")
        elif choice == '3':
            print("Product Cipher - Not yet implemented")
        elif choice == '0':
            print("Thank you for using the program!")
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
