"""
Caesar Cipher Implementation with Bigram Analysis
Two Brute Force Attack Algorithms:
1. Exhaustive Search
2. Frequency Analysis with Bigram Support
"""

def encrypt(plaintext, key):
    """
    Mã hóa Caesar cipher.
    
    Args:
        plaintext (str): Văn bản gốc
        key (int): Khóa dịch chuyển (0-25)
    
    Returns:
        str: Văn bản mã hóa
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
    Giải mã Caesar cipher.
    
    Args:
        ciphertext (str): Văn bản mã hóa
        key (int): Khóa dịch chuyển (0-25)
    
    Returns:
        str: Văn bản gốc
    """
    return encrypt(ciphertext, (-key) % 26)


def brute_force_exhaustive(ciphertext):
    """
    Thử tất cả 26 khóa.
    
    Args:
        ciphertext (str): Văn bản mã hóa
    
    Returns:
        list: [(khóa, văn_bản_giải_mã), ...]
    """
    results = []
    
    for key in range(26):
        plaintext = decrypt(ciphertext, key)
        results.append((key, plaintext))
    
    return results


def brute_force_exhaustive_display(ciphertext):
    """Display exhaustive search results."""
    results = brute_force_exhaustive(ciphertext)
    
    print("\n" + "=" * 100)
    print("EXHAUSTIVE SEARCH (TRY ALL 26 KEYS)")
    print("=" * 100)
    print(f"Ciphertext: {ciphertext}\n")
    print(f"{'Key':<5} {'Decrypted Text'}")
    print("-" * 100)
    
    for key, plaintext in results:
        print(f"{key:<5} {plaintext}")
    
    print("-" * 100)


def analyze_frequency(text):
    """Analyze character frequency."""
    freq = {}
    for char in text.lower():
        if char.isalpha():
            freq[char] = freq.get(char, 0) + 1
    return freq


def analyze_bigram_frequency(text):
    """
    Analyze bigram frequency (consecutive character pairs).
    
    Args:
        text (str): Text to analyze
    
    Returns:
        dict: {bigram: frequency_count}
    """
    text = text.lower()
    bigram_freq = {}
    for i in range(len(text) - 1):
        char1 = text[i]
        char2 = text[i + 1]
        if char1.isalpha() and char2.isalpha():
            bigram = char1 + char2
            bigram_freq[bigram] = bigram_freq.get(bigram, 0) + 1
    
    return bigram_freq


def standard_english_freq():
    """Standard English letter frequency (%) from large corpus."""
    return {
        'a': 8.167,  'b': 1.492,  'c': 2.782,  'd': 4.253,
        'e': 12.702, 'f': 2.228,  'g': 2.015,  'h': 6.094,
        'i': 6.966,  'j': 0.153,  'k': 0.772,  'l': 4.025,
        'm': 2.406,  'n': 6.749,  'o': 7.507,  'p': 1.929,
        'q': 0.095,  'r': 5.987,  's': 6.327,  't': 9.056,
        'u': 2.758,  'v': 0.978,  'w': 2.360,  'x': 0.150,
        'y': 1.974,  'z': 0.074
    }


def standard_english_bigram_freq():
    """
    Tần suất BIGRAM tiêu chuẩn tiếng Anh (%).
    Dữ liệu từ phân tích corpus tiếng Anh lớn.
    CHỈ DÙNG BIGRAM (2 CHỮCÁI) ĐỂ TRÁNH LỖI.
    
    Returns:
        dict: {bigram: tần_suất_%}
    """
    return {
        # Top 20 bigrams
        'th': 3.88,
        'he': 3.68,
        'in': 2.28,
        'er': 2.04,
        'an': 1.99,
        'ed': 1.67,
        'nd': 1.61,
        'to': 1.45,
        'en': 1.45,
        'ti': 1.37,
        'es': 1.32,
        'or': 1.32,
        'te': 1.31,
        'ar': 1.30,
        'ou': 1.28,
        'it': 1.24,
        'ha': 1.21,
        'et': 1.15,
        'ng': 1.14,
        'on': 1.12,
        're': 1.10,
        'be': 1.07,
        'as': 1.03,
        'at': 1.02,
        'de': 0.97,
        'is': 0.93,
        'le': 0.87,
        'al': 0.87,
        'se': 0.85,
        'st': 0.84,
        'me': 0.76,
        'co': 0.74,
        'ca': 0.71,
        'by': 0.69,
        'il': 0.68,
        'un': 0.68,
        'ir': 0.65,
        'li': 0.64,
        'ce': 0.63,
        've': 0.63,
        'ra': 0.61,
        'so': 0.60,
        'la': 0.59,
        'ri': 0.58,
        'hi': 0.58,
        'ts': 0.56,
        'ol': 0.55,
        'ne': 0.54,
        'mi': 0.53,
        'fr': 0.52,
        'ro': 0.52,
        'ai': 0.51,
        'em': 0.50,
        'wa': 0.51,
        'tr': 0.50,
        'ur': 0.50,
        'ch': 0.50,
        'ho': 0.49,
        'dr': 0.20,
        'ae': 0.15,
        'xy': 0.10,
        'qx': 0.01,
        'zz': 0.01
    }


def chi_squared_test(observed_freq, expected_freq):
    """
    Chi-squared test: χ² = Σ [(O - E)² / E]
    Uses Laplace smoothing to avoid errors with short text.
    
    Args:
        observed_freq (dict): Observed frequency
        expected_freq (dict): Expected frequency (standard)
    
    Returns:
        float: Chi-squared score (lower is better)
    """
    chi_squared = 0
    total_observed = sum(observed_freq.values())
    for item in expected_freq:
        expected_count = (expected_freq[item] / 100) * total_observed
        observed_count = observed_freq.get(item, 0)
        expected_count += 0.5
        observed_count += 0.5
        if expected_count > 0:
            chi_squared += ((observed_count - expected_count) ** 2) / expected_count
    
    return chi_squared


def brute_force_frequency_analysis(ciphertext):
    """
    Frequency analysis using unigram approach.
    
    Args:
        ciphertext (str): Encrypted text
    
    Returns:
        tuple: (key, decrypted_text, chi_squared_score)
    """
    expected_freq = standard_english_freq()
    best_score = float('inf')
    best_key = 0
    best_plaintext = ciphertext
    for key in range(26):
        plaintext = decrypt(ciphertext, key)
        observed_freq = analyze_frequency(plaintext)
        score = chi_squared_test(observed_freq, expected_freq)
        
        if score < best_score:
            best_score = score
            best_key = key
            best_plaintext = plaintext
    
    return (best_key, best_plaintext, best_score)


def brute_force_frequency_analysis_bigram(ciphertext):
    """
    Adaptive frequency analysis: unigram for short text, unigram+bigram for long text.
    
    Args:
        ciphertext (str): Encrypted text
    
    Returns:
        tuple: (key, decrypted_text, score)
    """
    expected_freq = standard_english_freq()
    char_count = sum(1 for c in ciphertext if c.isalpha())
    
    if char_count < 100:
        best_score = float('inf')
        best_key = 0
        best_plaintext = ciphertext
        
        for key in range(26):
            plaintext = decrypt(ciphertext, key)
            observed_freq = analyze_frequency(plaintext)
            score = chi_squared_test(observed_freq, expected_freq)
            
            if score < best_score:
                best_score = score
                best_key = key
                best_plaintext = plaintext
        
        return (best_key, best_plaintext, best_score)
    
    else:
        expected_bigram_freq = standard_english_bigram_freq()
        best_score = float('inf')
        best_key = 0
        best_plaintext = ciphertext
        for key in range(26):
            plaintext = decrypt(ciphertext, key)
            observed_freq = analyze_frequency(plaintext)
            observed_bigram_freq = analyze_bigram_frequency(plaintext)
            score_unigram = chi_squared_test(observed_freq, expected_freq)
            score_bigram = chi_squared_test(observed_bigram_freq, expected_bigram_freq)
            combined_score = 0.4 * score_unigram + 0.6 * score_bigram
            
            if combined_score < best_score:
                best_score = combined_score
                best_key = key
                best_plaintext = plaintext
        
        return (best_key, best_plaintext, best_score)


def brute_force_frequency_analysis_top_n(ciphertext, n=5):
    """Top N khóa hàng đầu (phương pháp cũ - ký tự đơn)."""
    expected_freq = standard_english_freq()
    results = []
    
    for key in range(26):
        plaintext = decrypt(ciphertext, key)
        observed_freq = analyze_frequency(plaintext)
        score = chi_squared_test(observed_freq, expected_freq)
        results.append((key, plaintext, score))
    
    results.sort(key=lambda x: x[2])
    return results[:n]


def brute_force_frequency_analysis_bigram_top_n(ciphertext, n=5):
    """Top N khóa hàng đầu (phương pháp mới - BIGRAM)."""
    expected_bigram_freq = standard_english_bigram_freq()
    results = []
    
    for key in range(26):
        plaintext = decrypt(ciphertext, key)
        observed_bigram_freq = analyze_bigram_frequency(plaintext)
        score = chi_squared_test(observed_bigram_freq, expected_bigram_freq)
        results.append((key, plaintext, score))
    
    results.sort(key=lambda x: x[2])
    return results[:n]


def brute_force_frequency_analysis_display(ciphertext, show_top=5):
    """Display frequency analysis results (unigram method)."""
    key, plaintext, score = brute_force_frequency_analysis(ciphertext)
    top_candidates = brute_force_frequency_analysis_top_n(ciphertext, show_top)
    print("\n" + "=" * 100)
    print("FREQUENCY ANALYSIS RESULTS (UNIGRAM)")
    print("=" * 100)
    print(f"Ciphertext: {ciphertext}")
    print(f"Best key: {key}\n")
    
    print(f"{'Rank':<5} {'Key':<7} {'Chi-Squared':<16} {'Decrypted Text'}")
    print("-" * 100)
    
    for rank, (k, pt, sc) in enumerate(top_candidates, 1):
        marker = " [BEST KEY]" if k == key else ""
        print(f"{rank:<5} {k:<7} {sc:<16.4f} {pt}{marker}")
    
    print("-" * 100)
    print(f"\nFull decrypted text (Key {key}):")
    print(plaintext)


def brute_force_frequency_analysis_bigram_display(ciphertext, show_top=5):
    """Display frequency analysis results (unigram + bigram method)."""
    key, plaintext, score = brute_force_frequency_analysis_bigram(ciphertext)
    top_candidates = brute_force_frequency_analysis_bigram_top_n(ciphertext, show_top)
    text_length = sum(1 for c in ciphertext if c.isalpha())
    print("\n" + "=" * 110)
    print("FREQUENCY ANALYSIS RESULTS (UNIGRAM + BIGRAM)")
    print("=" * 110)
    print(f"Text length: {text_length} characters")
    print(f"Ciphertext: {ciphertext}\n")
    
    print(f"{'Rank':<5} {'Key':<7} {'Score':<16} {'Decrypted Text'}")
    print("-" * 110)
    
    for rank, (k, pt, sc) in enumerate(top_candidates, 1):
        marker = " [BEST KEY]" if k == key else ""
        print(f"{rank:<5} {k:<7} {sc:<16.4f} {pt}{marker}")
    
    print("-" * 110)
    print(f"\nBEST RESULTS:")
    print(f"   Key found: {key}")
    print(f"   Combined Score (40% unigram + 60% bigram): {score:.4f}")
    print(f"\nFull decrypted text (Key {key}):")
    print(plaintext)


def encrypt_file(input_file, output_file, key):
    """Encrypt a file with the given key."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            plaintext = f.read()
        
        ciphertext = encrypt(plaintext, key)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(ciphertext)
        
        print(f"Encryption successful: {output_file}")
    except FileNotFoundError:
        print(f"Error: File not found - {input_file}")
    except Exception as e:
        print(f"Error: {e}")


def decrypt_file(input_file, output_file, key):
    """Decrypt a file with the given key."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            ciphertext = f.read()
        
        plaintext = decrypt(ciphertext, key)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(plaintext)
        
        print(f"Decryption successful: {output_file}")
    except FileNotFoundError:
        print(f"Error: File not found - {input_file}")
    except Exception as e:
        print(f"Error: {e}")

def _adaptive_frequency_top_n(ciphertext, n=5):
    """
    Adaptive top-N candidates:
    - short/medium text: unigram
    - long text: bigram
    """
    char_count = sum(1 for c in ciphertext if c.isalpha())
    if char_count < 100:
        return brute_force_frequency_analysis_top_n(ciphertext, n), "Unigram Frequency Analysis"
    else:
        return brute_force_frequency_analysis_bigram_top_n(ciphertext, n), "Unigram + Bigram Frequency Analysis"


def cryptanalyze_file_exhaustive(input_file, output_file):
    """
    Cryptanalysis for file using Exhaustive Search.
    - Tries all 26 keys
    - Saves all candidates to output file
    - Also ranks them using chi-squared for easier reading
    """
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            ciphertext = f.read()

        expected_freq = standard_english_freq()
        results = []

        for key, plaintext in brute_force_exhaustive(ciphertext):
            observed_freq = analyze_frequency(plaintext)
            score = chi_squared_test(observed_freq, expected_freq)
            results.append((key, plaintext, score))

        results.sort(key=lambda x: x[2])
        best_key, best_plaintext, best_score = results[0]

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("=== CAESAR CRYPTANALYSIS RESULT (EXHAUSTIVE SEARCH) ===\n")
            f.write(f"Best key (ranked by chi-squared): {best_key}\n")
            f.write(f"Best score: {best_score:.4f}\n\n")

            f.write("All 26 candidates:\n")
            f.write("-" * 100 + "\n")
            f.write(f"{'Rank':<5} {'Key':<7} {'Chi-Squared':<16} {'Decrypted Text'}\n")
            f.write("-" * 100 + "\n")

            for rank, (key, plaintext, score) in enumerate(results, start=1):
                marker = " [BEST KEY]" if key == best_key else ""
                preview = plaintext[:120].replace("\n", " ")
                f.write(f"{rank:<5} {key:<7} {score:<16.4f} {preview}{marker}\n")

            f.write("-" * 100 + "\n")
            f.write(f"\nRecovered plaintext (best candidate, key={best_key}):\n")
            f.write(best_plaintext)

        print(f"Exhaustive cryptanalysis result saved to: {output_file}")
        print(f"Recovered key: {best_key}")

    except FileNotFoundError:
        print(f"Error: File not found - {input_file}")
    except Exception as e:
        print(f"Error: {e}")


def cryptanalyze_file_frequency(input_file, output_file, top_n=5):
    """
    Cryptanalysis for file using Frequency Analysis.
    - Uses adaptive method:
      short/medium text -> unigram
      long text -> unigram + bigram
    - Saves best candidate and top-N ranking to output file
    """
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            ciphertext = f.read()

        recommendation = recommend_analysis_method(ciphertext)
        top_candidates, method_name = _adaptive_frequency_top_n(ciphertext, top_n)

        char_count = sum(1 for c in ciphertext if c.isalpha())
        if char_count < 100:
            best_key, best_plaintext, best_score = brute_force_frequency_analysis(ciphertext)
        else:
            best_key, best_plaintext, best_score = brute_force_frequency_analysis_bigram(ciphertext)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("=== CAESAR CRYPTANALYSIS RESULT (FREQUENCY ANALYSIS) ===\n")
            f.write(f"Recommended method: {recommendation['method']}\n")
            f.write(f"Confidence: {recommendation['confidence']}\n")
            f.write(f"Characters analyzed: {recommendation['char_count']}\n")
            f.write(f"Method used: {method_name}\n")
            f.write(f"Recovered key: {best_key}\n")
            f.write(f"Best score: {best_score:.4f}\n\n")

            f.write(f"Top {len(top_candidates)} candidates:\n")
            f.write("-" * 100 + "\n")
            f.write(f"{'Rank':<5} {'Key':<7} {'Score':<16} {'Decrypted Text'}\n")
            f.write("-" * 100 + "\n")

            for rank, (key, plaintext, score) in enumerate(top_candidates, start=1):
                marker = " [BEST KEY]" if key == best_key else ""
                preview = plaintext[:120].replace("\n", " ")
                f.write(f"{rank:<5} {key:<7} {score:<16.4f} {preview}{marker}\n")

            f.write("-" * 100 + "\n")
            f.write(f"\nRecovered plaintext (best candidate, key={best_key}):\n")
            f.write(best_plaintext)

        print(f"Frequency cryptanalysis result saved to: {output_file}")
        print(f"Recovered key: {best_key}")

    except FileNotFoundError:
        print(f"Error: File not found - {input_file}")
    except Exception as e:
        print(f"Error: {e}")


def recommend_analysis_method(ciphertext):
    """
    Recommend attack method based on text length.
    
    Args:
        ciphertext (str): Encrypted text
    
    Returns:
        dict: Recommendation info with keys: method, confidence, recommendation, char_count
    """
    char_count = sum(1 for c in ciphertext if c.isalpha())
    if char_count < 20:
        return {
            'method': 'Exhaustive Search',
            'confidence': 'GUARANTEED (100%)',
            'recommendation': f'Text too short ({char_count} chars). Use exhaustive search.',
            'char_count': char_count
        }
    elif char_count < 50:
        return {
            'method': 'Exhaustive + Frequency Analysis',
            'confidence': 'LOW (50-60%)',
            'recommendation': f'Short text ({char_count} chars). Try exhaustive search first.',
            'char_count': char_count
        }
    elif char_count < 100:
        return {
            'method': 'Unigram Frequency Analysis',
            'confidence': 'MEDIUM-HIGH (70-85%)',
            'recommendation': f'Medium text ({char_count} chars). Use unigram analysis.',
            'char_count': char_count
        }
    else:
        return {
            'method': 'Unigram + Bigram Analysis',
            'confidence': 'HIGH (85-95%)',
            'recommendation': f'Long text ({char_count} chars). Use unigram + bigram analysis.',
            'char_count': char_count
        }
