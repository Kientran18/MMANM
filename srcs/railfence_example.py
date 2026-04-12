"""
Example usage of Rail Fence Cipher
This file demonstrates encryption, decryption, and smart cryptanalysis.
"""

import railfence

def run_demonstration():
    print("=" * 60)
    print("RAIL FENCE CIPHER - SYSTEM DEMONSTRATION")
    print("=" * 60)

    # --- Ví dụ 1: Mã hóa và Giải mã cơ bản ---
    print("\n[Example 1: Basic Encryption & Decryption]")
    print("-" * 40)
    
    plaintext = "The cryptography is the practice and study of techniques for secure communication."
    key = 3
    
    # Sử dụng hàm trực tiếp
    ciphertext = railfence.encrypt_railfence(plaintext, key)
    decrypted = railfence.decrypt_railfence(ciphertext, key)
    
    print(f"Original Text:  {plaintext}")
    print(f"Secret Key:     {key}")
    print(f"Ciphertext:     {ciphertext}")
    print(f"Decrypted:      {decrypted}")
    print(f"Verification:   {'SUCCESS' if plaintext == decrypted else 'FAILED'}")


    # --- Ví dụ 2: Thám mã thông minh (Không cần biết khóa) ---
    print("\n" + "=" * 60)
    print("[Example 2: Smart Cryptanalysis (Brute Force + NLTK)]")
    print("-" * 40)
    
    # Giả sử ta thu được bản mã này từ một nguồn bí mật
    mystery_cipher = "T rph i h rcia dtu fthiqsfrsu emnc t oye tgapys te pcceansdyo ecnue o euecmiaio.h tnt nfo rcn"
    print(f"Received Ciphertext: {mystery_cipher}")
    print("\nStarting automated attack...")

    # Khởi tạo đối tượng hệ thống để lưu trữ kết quả thám mã
    rf_system = railfence.RailFenceSystem()
    
    # Tiến hành thám mã thử các khóa từ 2 đến 10
    rf_system.railfence_cryptanalyze(mystery_cipher, max_key=20)
    
    print("\n--- FINAL DISCOVERY ---")
    print(f"Recovered Key:  {rf_system.RailFence_Recovered_Key}")
    print(f"Recovered Text: {rf_system.RailFence_Recovered_Text}")


    # --- Ví dụ 3: Sự bảo toàn tần suất ký tự ---
    print("\n" + "=" * 60)
    print("[Example 3: Transposition Property (Frequency Analysis)]")
    print("-" * 40)
    
    # So sánh tần suất chữ 'e' và 't' để chứng minh đây là mã hoán vị
    def quick_count(text, char):
        return text.lower().count(char.lower())

    char_to_test = 'e'
    print(f"Character '{char_to_test}' in Plaintext:  {quick_count(plaintext, char_to_test)} times")
    print(f"Character '{char_to_test}' in Ciphertext: {quick_count(ciphertext, char_to_test)} times")
    print("\nNote: Frequency remains identical, only the order is scrambled!")

if __name__ == "__main__":
    run_demonstration()