"""
Example usage of Caesar Cipher
This file demonstrates how to use the caesar module
"""

import caesar

print("=" * 50)
print("Example 1: Simple Text Encryption")
print("=" * 50)

plaintext = "The Quick Brown Fox Jumps Over The Lazy Dog"
key = 5

ciphertext = caesar.encrypt(plaintext, key)
decrypted = caesar.decrypt(ciphertext, key)

print(f"Original:  {plaintext}")
print(f"Key:       {key}")
print(f"Encrypted: {ciphertext}")
print(f"Decrypted: {decrypted}")
print(f"Match:     {plaintext == decrypted}")

print("\n" + "=" * 50)
print("Example 2: Brute Force Attack")
print("=" * 50)

mystery_text = "Uryyb Jbeyq"
print(f"Mystery text: {mystery_text}")
print("\nTrying all possible keys:")

results = caesar.brute_force(mystery_text)
for k, text in results:
    if k in [0, 1, 5, 7]: 
        print(f"  Key {k:2d}: {text}")
    elif k == 2:
        print(f"  ...")

print("\n" + "=" * 50)
print("Example 3: Frequency Analysis")
print("=" * 50)

sample_text = """
The Caesar cipher is a simple substitution cipher where each letter
is shifted by a fixed number of positions in the alphabet. This method
is named after Julius Caesar. Although Caesar cipher is very simple,
it is not secure for practical use.
"""

freq = caesar.analyze_frequency(sample_text)
print("\nTop 5 most frequent characters:")

sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
for i, (char, count) in enumerate(sorted_freq[:5], 1):
    total = sum(freq.values())
    percentage = (count / total) * 100
    print(f"  {i}. '{char}': {count} times ({percentage:.1f}%)")

print("\n" + "=" * 50)
print("Example 4: Encryption with Different Keys")
print("=" * 50)

text = "HELLO"
print(f"Original text: {text}\n")
print(f"{'Key':<5} {'Encrypted':<20}")
print("-" * 25)

for k in range(0, 26, 5):
    encrypted = caesar.encrypt(text, k)
    print(f"{k:<5} {encrypted:<20}")

print("\n" + "=" * 50)
print("Example 5: Special Characters and Numbers")
print("=" * 50)

special_text = "Hello, World! 123 #@!"
encrypted_special = caesar.encrypt(special_text, 3)

print(f"Original:  {special_text}")
print(f"Encrypted: {encrypted_special}")
print(f"\nNote: Numbers and special characters are preserved!")
