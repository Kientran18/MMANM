

import os
from caesar import (
    encrypt,
    decrypt,
    brute_force_exhaustive_display,
    brute_force_frequency_analysis_display,
    encrypt_file,
    decrypt_file
)


def caesar_menu():
    
    while True:
        print("\n" + "=" * 70)
        print("CAESAR CIPHER - BRUTE FORCE ATTACK")
        print("=" * 70)
        print("1. Mã hóa văn bản")
        print("2. Giải mã văn bản")
        print("3. Duyệt Cạn (Exhaustive Search)")
        print("4. Phân tích Tần suất (Frequency Analysis)")
        print("5. Mã hóa file")
        print("6. Giải mã file")
        print("0. Quay lại")
        print("=" * 70)
        
        choice = input("Chọn chức năng (0-6): ").strip()
        
        if choice == "1":
            # Mã hóa
            plaintext = input("\nNhập văn bản gốc: ")
            try:
                key = int(input("Nhập khóa (0-25): "))
                if 0 <= key <= 25:
                    ciphertext = encrypt(plaintext, key)
                    print(f"\n Văn bản mã hóa: {ciphertext}")
                else:
                    print(" Khóa phải trong khoảng 0-25!")
            except ValueError:
                print(" Khóa phải là số nguyên!")
        
        elif choice == "2":
            # Giải mã
            ciphertext = input("\nNhập văn bản mã hóa: ")
            try:
                key = int(input("Nhập khóa (0-25): "))
                if 0 <= key <= 25:
                    plaintext = decrypt(ciphertext, key)
                    print(f"\n Văn bản giải mã: {plaintext}")
                else:
                    print(" Khóa phải trong khoảng 0-25!")
            except ValueError:
                print(" Khóa phải là số nguyên!")
        
        elif choice == "3":
            ciphertext = input("\nNhập văn bản mã hóa: ")
            brute_force_exhaustive_display(ciphertext)
            input("Nhấn Enter để tiếp tục...")
        
        elif choice == "4":
            ciphertext = input("\nNhập văn bản mã hóa: ")
            try:
                top_n = int(input("Hiển thị top bao nhiêu khóa? (mặc định 5): ") or "5")
                brute_force_frequency_analysis_display(ciphertext, top_n)
            except ValueError:
                brute_force_frequency_analysis_display(ciphertext, 5)
            input("Nhấn Enter để tiếp tục...")
        
        elif choice == "5":
            input_file = input("\nNhập đường dẫn file gốc (mặc định: data/plaintext.txt): ").strip() or "data/plaintext.txt"
            output_file = input("Nhập đường dẫn file mã hóa (mặc định: data/ciphertext.txt): ").strip() or "data/ciphertext.txt"
            try:
                key = int(input("Nhập khóa (0-25): "))
                if 0 <= key <= 25:
                    encrypt_file(input_file, output_file, key)
                    print(f" Khóa được sử dụng: {key}")
                else:
                    print(" Khóa phải trong khoảng 0-25!")
            except ValueError:
                print(" Khóa phải là số nguyên!")
        
        elif choice == "6":
            input_file = input("\nNhập đường dẫn file mã hóa (mặc định: data/ciphertext.txt): ").strip() or "data/ciphertext.txt"
            output_file = input("Nhập đường dẫn file giải mã (mặc định: data/decrypted.txt): ").strip() or "data/decrypted.txt"
            try:
                key = int(input("Nhập khóa (0-25): "))
                if 0 <= key <= 25:
                    decrypt_file(input_file, output_file, key)
                    print(f"✓ Khóa được sử dụng: {key}")
                else:
                    print("✗ Khóa phải trong khoảng 0-25!")
            except ValueError:
                print("✗ Khóa phải là số nguyên!")
        
        elif choice == "0":
            print("Quay lại menu chính...\n")
            break
        
        else:
            print("✗ Lựa chọn không hợp lệ!")


def main():
    """Menu chính."""
    
    while True:
        print("\n" + "=" * 70)
        print("MÃ HÓA - GIẢI MÃ VÀ TẤN CÔNG")
        print("=" * 70)
        print("1. Caesar Cipher (Duyệt Cạn + Phân tích Tần suất)")
        print("2. Rail Fence Cipher (Sắp tới...)")
        print("3. Product Cipher (Sắp tới...)")
        print("0. Thoát")
        print("=" * 70)
        
        choice = input("Chọn mã hóa (0-3): ").strip()
        
        if choice == "1":
            caesar_menu()
        elif choice == "2":
            print("\n Rail Fence Cipher sẽ sớm được phát triển...")
        elif choice == "3":
            print("\n Product Cipher sẽ sớm được phát triển...")
        elif choice == "0":
            print("\n Tạm biệt!\n")
            break
        else:
            print("✗ Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()
