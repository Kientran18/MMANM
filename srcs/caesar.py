"""
Caesar Cipher Implementation
This module provides encryption, decryption, and cryptanalysis functions for the Caesar cipher.
"""

def encrypt(plaintext, key):
    """
    Encrypt plaintext using Caesar cipher with given key.
    
    Args:
        plaintext (str): The text to encrypt
        key (int): The shift value (0-25)
    
    Returns:
        str: The encrypted text
    """
    ciphertext = ""
    
    for char in plaintext:
        if char.isalpha():
            if char.isupper():
                shifted = (ord(char) - ord('A') + key) % 26
                ciphertext += chr(shifted + ord('A'))
            else:
                shifted = (ord(char) - ord('a') + key) % 26
                ciphertext += chr(shifted + ord('a'))
        else:
            ciphertext += char
    
    return ciphertext


def decrypt(ciphertext, key):
    """
    Decrypt ciphertext using Caesar cipher with given key.
    
    Args:
        ciphertext (str): The text to decrypt
        key (int): The shift value (0-25)
    
    Returns:
        str: The decrypted text
    """
    return encrypt(ciphertext, (-key) % 26)


def brute_force(ciphertext):
    """
    Attempt to break Caesar cipher by trying all possible keys.
    
    Args:
        ciphertext (str): The text to decrypt
    
    Returns:
        list: List of tuples (key, decrypted_text) for all possible shifts
    """
    results = []
    for key in range(26):
        plaintext = decrypt(ciphertext, key)
        results.append((key, plaintext))
    return results


def brute_force_display(ciphertext):
    """
    Display all possible decryptions from brute force attack.
    
    Args:
        ciphertext (str): The text to decrypt
    """
    results = brute_force(ciphertext)
    print(f"{'Key':<5} {'Plaintext':<50}")
    print("-" * 55)
    for key, plaintext in results:
        print(f"{key:<5} {plaintext:<50}")


def encrypt_file(input_file, output_file, key):
    """
    Encrypt a file using Caesar cipher.
    
    Args:
        input_file (str): Path to input file
        output_file (str): Path to output file
        key (int): The shift value (0-25)
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            plaintext = f.read()
        
        ciphertext = encrypt(plaintext, key)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(ciphertext)
        
        print(f"✓ File encrypted successfully: {output_file}")
    except FileNotFoundError:
        print(f"✗ Error: File not found - {input_file}")
    except Exception as e:
        print(f"✗ Error: {e}")


def decrypt_file(input_file, output_file, key):
    """
    Decrypt a file using Caesar cipher.
    
    Args:
        input_file (str): Path to input file
        output_file (str): Path to output file
        key (int): The shift value (0-25)
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            ciphertext = f.read()
        
        plaintext = decrypt(ciphertext, key)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(plaintext)
        
        print(f"✓ File decrypted successfully: {output_file}")
    except FileNotFoundError:
        print(f"✗ Error: File not found - {input_file}")
    except Exception as e:
        print(f"✗ Error: {e}")


def analyze_frequency(text):
    """
    Analyze character frequency in text (useful for cryptanalysis).
    
    Args:
        text (str): The text to analyze
    
    Returns:
        dict: Dictionary with character frequencies
    """
    freq = {}
    for char in text.lower():
        if char.isalpha():
            freq[char] = freq.get(char, 0) + 1
    
    # Sort by frequency
    sorted_freq = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
    return sorted_freq


def print_frequency(freq_dict):
    """
    Print character frequency analysis.
    
    Args:
        freq_dict (dict): Dictionary with character frequencies
    """
    print("Character Frequency Analysis:")
    print(f"{'Char':<5} {'Count':<10} {'Percentage':<10}")
    print("-" * 25)
    
    total = sum(freq_dict.values())
    for char, count in freq_dict.items():
        percentage = (count / total) * 100
        print(f"{char:<5} {count:<10} {percentage:.2f}%")
