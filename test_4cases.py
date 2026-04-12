#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test 4 Test Cases cho Caesar Cipher Frequency Analysis
Kiểm tra cải tiến: Text < 100 chữ → Unigram only, Text >= 100 chữ → Unigram + Bigram
"""

import sys
sys.path.insert(0, 'srcs')

from caesar.caesar import encrypt, decrypt, brute_force_frequency_analysis_bigram, analyze_frequency, chi_squared_test

def test_case(name, plaintext, key):
    """Test một case"""
    print(f"\n{'='*70}")
    print(f"TEST CASE: {name}")
    print(f"{'='*70}")
    
    # Mã hóa
    encrypted = encrypt(plaintext, key)
    alphabet_count = sum(1 for c in plaintext if c.isalpha())
    
    print(f"✓ Plaintext length: {len(plaintext)} ({alphabet_count} alphabet chars)")
    print(f"✓ Encryption key: {key}")
    print(f"✓ First 50 chars of plaintext: {plaintext[:50]}")
    print(f"✓ First 50 chars of ciphertext: {encrypted[:50]}")
    
    # Phân tích
    print(f"\n➜ Running brute_force_frequency_analysis_bigram()...")
    found_key, found_plaintext, score = brute_force_frequency_analysis_bigram(encrypted)
    
    print(f"✓ Found key: {found_key}")
    print(f"✓ Score: {score:.4f}")
    
    # Check kết quả
    if found_key == key:
        print(f"✅ PASS - Correct key found!")
        return True
    else:
        print(f"❌ FAIL - Wrong key!")
        print(f"   Expected: {key}, Got: {found_key}")
        print(f"   First 50 chars of found plaintext: {found_plaintext[:50]}")
        return False

# ============================================
# TEST CASE 1: Long text (148 chars), key=7
# ============================================
print("\n" + "="*70)
print("TEST CASE 1: Long English Text (148 alphabet chars)")
print("="*70)

plaintext1 = "The learning planes in frost vary knowledge are flashed about this as when the fresh and free movements of the soul from thought all of the in the work are mixed may be happy"
key1 = 7
result1 = test_case("Case 1: Long Text", plaintext1, key1)

# ============================================
# TEST CASE 2: E-less text (55 chars), key=10
# ============================================
print("\n" + "="*70)
print("TEST CASE 2: Text without letter 'E' (55 alphabet chars)")
print("="*70)

plaintext2 = "Brown Fox jumping at moon wild dog sparks flying through morning Sun"
key2 = 10
result2 = test_case("Case 2: No-E Text", plaintext2, key2)

# ============================================
# TEST CASE 3: Short text (10 chars), key=13
# ============================================
print("\n" + "="*70)
print("TEST CASE 3: Very Short Text (10 alphabet chars)")
print("A")
print("="*70)

plaintext3 = "Hello John"
key3 = 13
result3 = test_case("Case 3: Short Text (EXPECTED TO FAIL)", plaintext3, key3)

# ============================================
# TEST CASE 4: Special chars (30 letters + 6 numbers), key=5
# ============================================
print("\n" + "="*70)
print("TEST CASE 4: Text with Special Characters (30 alphabet chars + numbers)")
print("="*70)

plaintext4 = "Hello World 123456 This is test"
key4 = 5
result4 = test_case("Case 4: Special Chars", plaintext4, key4)

# ============================================
# SUMMARY
# ============================================
print("\n" + "="*70)
print("SUMMARY")
print("="*70)

passed = sum([result1, result2, result3, result4])
total = 4

print(f"✅ Passed: {passed}/{total}")
print(f"❌ Failed: {total - passed}/{total}")

results = [
    ("Case 1 (148 chars, k=7): Long text → Unigram+Bigram", result1),
    ("Case 2 (55 chars, k=10): E-less text → Unigram only", result2),
    ("Case 3 (10 chars, k=13): Short text → EXPECTED FAIL", result3),
    ("Case 4 (30 chars, k=5): Special chars → Unigram only", result4),
]

for desc, result in results:
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"{status}: {desc}")

print()
