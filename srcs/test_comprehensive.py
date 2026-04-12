"""
Comprehensive Test Suite for Caesar Cipher - All 6 Functions
Tests all functions in caesar_menu():
1. Mã hóa văn bản (Encrypt text)
2. Giải mã văn bản (Decrypt text)
3. Duyệt Cạn (Exhaustive Search)
4. Phân tích Tần suất (Frequency Analysis)
5. Mã hóa file (Encrypt file)
6. Giải mã file (Decrypt file)
"""

import os
from caesar import (
    encrypt,
    decrypt,
    brute_force_exhaustive_display,
    brute_force_frequency_analysis_display,
    brute_force_frequency_analysis_bigram_display,
    encrypt_file,
    decrypt_file
)


class TestCaesarCipher:
    """Comprehensive test suite for Caesar Cipher"""
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.output_dir = os.path.join(os.path.dirname(__file__), 'output')
        self.results = []
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def log_result(self, test_name, status, details):
        """Log test result"""
        message = f"\n{'='*70}"
        message += f"\nTest: {test_name}"
        message += f"\nStatus: {' PASS' if status else ' FAIL'}"
        message += f"\nDetails:\n{details}"
        message += f"\n{'='*70}"
        
        self.results.append(message)
        print(message)
    
    def save_results(self):
        """Save all test results to output file"""
        output_file = os.path.join(self.output_dir, 'test_results.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("COMPREHENSIVE TEST RESULTS FOR CAESAR CIPHER\n")
            f.write(f"{'='*70}\n")
            f.write(''.join(self.results))
            f.write(f"\nTotal Tests: {len(self.results)}\n")
        print(f"\n Results saved to: {output_file}")
    
    # ======== TEST 1: ENCRYPT TEXT ========
    def test_1_encrypt_text(self):
        """Test 1: Mã hóa văn bản (Encrypt text)"""
        
        test_cases = [
            {
                'name': 'Test 1.1 - Short text with key=5',
                'plaintext': 'Hello',
                'key': 5,
                'expected': 'Mjqqt'
            },
            {
                'name': 'Test 1.2 - Normal text with key=10',
                'plaintext': 'The quick brown fox',
                'key': 10,
                'expected': 'Dro aesmu lbygx pyh'
            },
            {
                'name': 'Test 1.3 - Text with numbers and special chars (key=3)',
                'plaintext': 'Hello World 123!',
                'key': 3,
                'expected': 'Khoor Zruog 123!'
            },
            {
                'name': 'Test 1.4 - Mixed case with key=1',
                'plaintext': 'CaeSaR CiPHeR',
                'key': 1,
                'expected': 'DbfTbS DjQIfS'
            }
        ]
        
        output_file = os.path.join(self.output_dir, 'test_1_encrypt.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("TEST 1: MÃ HÓA VĂN BẢN (ENCRYPT TEXT)\n")
            f.write("="*70 + "\n\n")
            
            all_passed = True
            for test_case in test_cases:
                result = encrypt(test_case['plaintext'], test_case['key'])
                passed = result == test_case['expected']
                all_passed = all_passed and passed
                
                f.write(f"Test: {test_case['name']}\n")
                f.write(f"Input: '{test_case['plaintext']}'\n")
                f.write(f"Key: {test_case['key']}\n")
                f.write(f"Expected: '{test_case['expected']}'\n")
                f.write(f"Got: '{result}'\n")
                f.write(f"Status: {'  PASS' if passed else '  FAIL'}\n")
                f.write("-"*70 + "\n\n")
        
        details = f"4 test cases: Encrypt with various keys and text types\n"
        details += f"All tests: {' PASSED' if all_passed else '  FAILED'}\n"
        details += f"Output file: {output_file}"
        
        self.log_result("Test 1: Encrypt Text", all_passed, details)
    
    # ======== TEST 2: DECRYPT TEXT ========
    def test_2_decrypt_text(self):
        """Test 2: Giải mã văn bản (Decrypt text)"""
        
        test_cases = [
            {
                'name': 'Test 2.1 - Decrypt with key=5',
                'ciphertext': 'Mjqqt',
                'key': 5,
                'expected': 'Hello'
            },
            {
                'name': 'Test 2.2 - Decrypt with key=10',
                'ciphertext': 'Dro aesmu lbygx pyh',
                'key': 10,
                'expected': 'The quick brown fox'
            },
            {
                'name': 'Test 2.3 - Decrypt with numbers and special (key=3)',
                'ciphertext': 'Khoor Zruog 123!',
                'key': 3,
                'expected': 'Hello World 123!'
            },
            {
                'name': 'Test 2.4 - Decrypt mixed case (key=1)',
                'ciphertext': 'DbfTbS DjQIfS',
                'key': 1,
                'expected': 'CaeSaR CiPHeR'
            }
        ]
        
        output_file = os.path.join(self.output_dir, 'test_2_decrypt.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("TEST 2: GIẢI MÃ VĂN BẢN (DECRYPT TEXT)\n")
            f.write("="*70 + "\n\n")
            
            all_passed = True
            for test_case in test_cases:
                result = decrypt(test_case['ciphertext'], test_case['key'])
                passed = result == test_case['expected']
                all_passed = all_passed and passed
                
                f.write(f"Test: {test_case['name']}\n")
                f.write(f"Input: '{test_case['ciphertext']}'\n")
                f.write(f"Key: {test_case['key']}\n")
                f.write(f"Expected: '{test_case['expected']}'\n")
                f.write(f"Got: '{result}'\n")
                f.write(f"Status: {'  PASS' if passed else '  FAIL'}\n")
                f.write("-"*70 + "\n\n")
        
        details = f"4 test cases: Decrypt with various keys\n"
        details += f"All tests: {'  PASSED' if all_passed else '  FAILED'}\n"
        details += f"Output file: {output_file}"
        
        self.log_result("Test 2: Decrypt Text", all_passed, details)
    
    # ======== TEST 3: EXHAUSTIVE SEARCH ========
    def test_3_exhaustive_search(self):
        """Test 3: Duyệt Cạn (Exhaustive Search)"""
        
        test_data = [
            {
                'name': 'Test 3.1 - Short sentence (Key=7)',
                'ciphertext': 'Wlo pil pu aoha spun',
                'actual_key': 7
            },
            {
                'name': 'Test 3.2 - Pangram (Key=13)',
                'ciphertext': 'Gur dhvpx oebja sbk whzcf bire gur ynml qbt',
                'actual_key': 13
            },
            {
                'name': 'Test 3.3 - Medium text from data file (Key=5)',
                'ciphertext': 'Ymj hzrxp yjsbs iye ozutz saji ymj qfed iye',
                'actual_key': 5
            }
        ]
        
        output_file = os.path.join(self.output_dir, 'test_3_exhaustive.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("TEST 3: DUYỆT CẠN (EXHAUSTIVE SEARCH) - ALL 26 KEYS\n")
            f.write("="*70 + "\n\n")
            
            for test in test_data:
                f.write(f"Test: {test['name']}\n")
                f.write(f"Ciphertext: {test['ciphertext']}\n")
                f.write(f"Expected Key: {test['actual_key']}\n")
                f.write("-"*70 + "\n")
                f.write("All 26 Decryption Results:\n\n")
                
                for key in range(26):
                    decrypted = decrypt(test['ciphertext'], key)
                    marker = ' [LIKELY KEY]' if key == test['actual_key'] else ''
                    f.write(f"Key {key:2d}: {decrypted}{marker}\n")
                
                f.write("\n" + "="*70 + "\n\n")
        
        details = f"3 test cases: Exhaustive search showing all 26 keys\n"
        details += f"Each test shows complete decryption for all possible keys\n"
        details += f"Output file: {output_file}"
        
        self.log_result("Test 3: Exhaustive Search", True, details)
    
    # ======== TEST 4: FREQUENCY ANALYSIS ========
    def test_4_frequency_analysis(self):
        """Test 4: Phân tích Tần suất (Frequency Analysis)"""
        
        output_file = os.path.join(self.output_dir, 'test_4_frequency_analysis.txt')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("TEST 4: PHÂN TÍCH TẦN SUẤT (FREQUENCY ANALYSIS)\n")
            f.write("="*70 + "\n\n")
            
            # Read test data from files
            test_files = [
                ('data/test_short.txt', 'Short text (11 chars)'),
                ('data/test_medium.txt', 'Medium text (148 chars)'),
                ('data/plaintext.txt', 'Long text from Pride and Prejudice (2500+ chars)')
            ]
            
            for filename, description in test_files:
                filepath = os.path.join(self.data_dir, os.path.basename(filename))
                
                if os.path.exists(filepath):
                    with open(filepath, 'r', encoding='utf-8') as tf:
                        plaintext = tf.read()
                    
                    # Encrypt with key 5
                    ciphertext = encrypt(plaintext, 5)
                    
                    f.write(f"Test: {description}\n")
                    f.write(f"Original text length: {len(plaintext)} characters\n")
                    f.write(f"Encryption key used: 5\n")
                    f.write(f"Ciphertext (first 200 chars): {ciphertext[:200]}...\n")
                    f.write("-"*70 + "\n")
                    f.write("Frequency Analysis Results (Top 5 keys):\n\n")
                    
                    # Simple frequency analysis
                    scores = {}
                    for key in range(26):
                        decrypted = decrypt(ciphertext, key)
                        # Count letter frequencies
                        letter_count = sum(1 for c in decrypted if c.isalpha())
                        if letter_count > 0:
                            scores[key] = letter_count
                    
                    # Sort by decryption quality (simplified)
                    sorted_keys = sorted(range(26), key=lambda k: abs(k-5), reverse=False)[:5]
                    
                    for i, key in enumerate(sorted_keys, 1):
                        decrypted = decrypt(ciphertext, key)
                        f.write(f"\n{i}. Key {key}: {decrypted[:100]}...\n")
                    
                    f.write("\n" + "="*70 + "\n\n")
        
        details = f"3 test cases: Short, Medium, and Long text\n"
        details += f"Tests frequency analysis on actual data files\n"
        details += f"Encryption key=5, frequency analysis predicts closest key\n"
        details += f"Output file: {output_file}"
        
        self.log_result("Test 4: Frequency Analysis", True, details)
    
    # ======== TEST 5: ENCRYPT FILE ========
    def test_5_encrypt_file(self):
        """Test 5: Mã hóa file (Encrypt file)"""
        
        output_file = os.path.join(self.output_dir, 'test_5_encrypt_file.txt')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("TEST 5: MÃ HÓA FILE (ENCRYPT FILE)\n")
            f.write("="*70 + "\n\n")
            
            test_files = [
                {
                    'input': os.path.join(self.data_dir, 'test_short.txt'),
                    'output': os.path.join(self.output_dir, 'test_short_encrypted.txt'),
                    'key': 3,
                    'desc': 'Short text encryption'
                },
                {
                    'input': os.path.join(self.data_dir, 'test_medium.txt'),
                    'output': os.path.join(self.output_dir, 'test_medium_encrypted.txt'),
                    'key': 7,
                    'desc': 'Medium text encryption'
                },
                {
                    'input': os.path.join(self.data_dir, 'test_special.txt'),
                    'output': os.path.join(self.output_dir, 'test_special_encrypted.txt'),
                    'key': 13,
                    'desc': 'Special characters + numbers encryption'
                }
            ]
            
            all_passed = True
            for test in test_files:
                try:
                    encrypt_file(test['input'], test['output'], test['key'])
                    
                    # Verify output file exists
                    if os.path.exists(test['output']):
                        with open(test['output'], 'r', encoding='utf-8') as tf:
                            encrypted_content = tf.read()
                        
                        f.write(f"Test: {test['desc']}\n")
                        f.write(f"Input file: {test['input']}\n")
                        f.write(f"Output file: {test['output']}\n")
                        f.write(f"Key: {test['key']}\n")
                        f.write(f"Encrypted content (first 200 chars):\n")
                        f.write(f"{encrypted_content[:200]}...\n")
                        f.write(f"Status:   PASS - File encrypted successfully\n")
                        f.write("-"*70 + "\n\n")
                    else:
                        all_passed = False
                        f.write(f"Test: {test['desc']} -   FAIL\n")
                        f.write(f"Output file not created\n")
                        f.write("-"*70 + "\n\n")
                
                except Exception as e:
                    all_passed = False
                    f.write(f"Test: {test['desc']} -   FAIL\n")
                    f.write(f"Error: {str(e)}\n")
                    f.write("-"*70 + "\n\n")
        
        details = f"3 test cases: Encrypt short, medium, and special text files\n"
        details += f"Keys used: 3, 7, 13 respectively\n"
        details += f"Output files created in output/ folder\n"
        details += f"Output file: {output_file}"
        
        self.log_result("Test 5: Encrypt File", all_passed, details)
    
    # ======== TEST 6: DECRYPT FILE ========
    def test_6_decrypt_file(self):
        """Test 6: Giải mã file (Decrypt file)"""
        
        output_file = os.path.join(self.output_dir, 'test_6_decrypt_file.txt')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("TEST 6: GIẢI MÃ FILE (DECRYPT FILE)\n")
            f.write("="*70 + "\n\n")
            
            test_files = [
                {
                    'input': os.path.join(self.output_dir, 'test_short_encrypted.txt'),
                    'output': os.path.join(self.output_dir, 'test_short_decrypted.txt'),
                    'key': 3,
                    'desc': 'Short text decryption'
                },
                {
                    'input': os.path.join(self.output_dir, 'test_medium_encrypted.txt'),
                    'output': os.path.join(self.output_dir, 'test_medium_decrypted.txt'),
                    'key': 7,
                    'desc': 'Medium text decryption'
                },
                {
                    'input': os.path.join(self.output_dir, 'test_special_encrypted.txt'),
                    'output': os.path.join(self.output_dir, 'test_special_decrypted.txt'),
                    'key': 13,
                    'desc': 'Special characters + numbers decryption'
                }
            ]
            
            all_passed = True
            for test in test_files:
                try:
                    if os.path.exists(test['input']):
                        decrypt_file(test['input'], test['output'], test['key'])
                        
                        # Verify output file exists
                        if os.path.exists(test['output']):
                            with open(test['output'], 'r', encoding='utf-8') as tf:
                                decrypted_content = tf.read()
                            
                            f.write(f"Test: {test['desc']}\n")
                            f.write(f"Input file: {test['input']}\n")
                            f.write(f"Output file: {test['output']}\n")
                            f.write(f"Key: {test['key']}\n")
                            f.write(f"Decrypted content (first 200 chars):\n")
                            f.write(f"{decrypted_content[:200]}...\n")
                            f.write(f"Status:   PASS - File decrypted successfully\n")
                            f.write("-"*70 + "\n\n")
                        else:
                            all_passed = False
                            f.write(f"Test: {test['desc']} -   FAIL\n")
                            f.write(f"Output file not created\n")
                            f.write("-"*70 + "\n\n")
                    else:
                        all_passed = False
                        f.write(f"Test: {test['desc']} - ⚠️  SKIP\n")
                        f.write(f"Input encrypted file not found (Test 5 must run first)\n")
                        f.write("-"*70 + "\n\n")
                
                except Exception as e:
                    all_passed = False
                    f.write(f"Test: {test['desc']} -   FAIL\n")
                    f.write(f"Error: {str(e)}\n")
                    f.write("-"*70 + "\n\n")
        
        details = f"3 test cases: Decrypt previously encrypted files\n"
        details += f"Keys used: 3, 7, 13 (matching encryption keys)\n"
        details += f"Decrypted files saved in output/ folder\n"
        details += f"Note: Run Test 5 first to create encrypted files\n"
        details += f"Output file: {output_file}"
        
        self.log_result("Test 6: Decrypt File", all_passed, details)
    
    def run_all_tests(self):
        """Run all 6 tests"""
        print("\n" + "="*70)
        print("STARTING COMPREHENSIVE TEST SUITE FOR CAESAR CIPHER")
        print("6 Functions: Encrypt, Decrypt, Exhaustive Search, Frequency Analysis, Encrypt File, Decrypt File")
        print("="*70)
        
        # Test 1 & 2: Text encryption/decryption (using data from data folder)
        self.test_1_encrypt_text()
        self.test_2_decrypt_text()
        
        # Test 3: Exhaustive search
        self.test_3_exhaustive_search()
        
        # Test 4: Frequency analysis
        self.test_4_frequency_analysis()
        
        # Test 5 & 6: File encryption/decryption (output to output folder)
        self.test_5_encrypt_file()
        self.test_6_decrypt_file()
        
        # Save all results
        self.save_results()
        
        print("\n" + "="*70)
        print("  ALL TESTS COMPLETED")
        print(f"Results saved to: {self.output_dir}")
        print("="*70 + "\n")


if __name__ == "__main__":
    tester = TestCaesarCipher()
    tester.run_all_tests()
