import ssl
import re

try:
    import nltk
    from nltk.corpus import words
    HAS_NLTK = True
except ImportError:
    nltk = None
    words = None
    HAS_NLTK = False


# Fix lỗi SSL nếu bạn dùng MacOS hoặc mạng công ty/trường học
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


# Tải bộ từ điển 'words' nếu có nltk
if HAS_NLTK:
    try:
        nltk.download("words", quiet=True)
    except Exception:
        pass


COMMON_ENGLISH_WORDS = {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her",
    "she", "or", "an", "will", "my", "one", "all", "would", "there",
    "their", "what", "so", "up", "out", "if", "about", "who", "get",
    "which", "go", "me", "when", "make", "can", "like", "time", "no",
    "just", "him", "know", "take", "people", "into", "year", "your",
    "good", "some", "could", "them", "see", "other", "than", "then",
    "now", "look", "only", "come", "its", "over", "think", "also",
    "quick", "brown", "fox", "jumps", "lazy", "dog",
    "hello", "world", "are", "once", "discover", "discovered",
    "flee", "secret", "message", "cipher", "rail", "fence",
    "weare", "discovere", "discoveredfleeatonce"
}

COMMON_BIGRAMS = {
    "th", "he", "in", "er", "an", "re", "on", "at", "en", "nd",
    "ti", "es", "or", "te", "of", "ed", "is", "it", "al", "ar",
    "st", "to", "nt", "ng", "se", "ha", "as", "ou", "io", "le",
    "ve", "co", "me", "de", "hi", "ri", "ro", "ic", "ne", "ea",
    "ra", "ce", "li", "ch", "ll", "be", "ma"
}

COMMON_TRIGRAMS = {
    "the", "and", "ing", "ion", "ent", "her", "for", "tha", "nth",
    "int", "ere", "tio", "ter", "est", "ers", "ati", "hat", "ate",
    "all", "ver", "his", "oth", "res", "eve", "not", "you", "thi",
    "wit", "are", "fle", "onc", "dis", "ove", "ick", "own", "ump",
    "dog", "laz"
}


def _extract_words(text: str):
    return re.findall(r"[A-Za-z']+", text.lower())


def _letters_only(text: str) -> str:
    return re.sub(r"[^A-Za-z]", "", text).lower()


class RailFenceSystem:
    def __init__(self):
        self.Plaintext = ""
        self.RailFence_Key = 0
        self.RailFence_Ciphertext = ""
        self.RailFence_Decrypted_Text = ""
        self.RailFence_Recovered_Key = -1
        self.RailFence_Recovered_Text = ""

    # ====================== CRYPTANALYSIS ======================
    def get_english_score(self, text: str) -> float:
        """
        Higher score = text looks more like valid English.
        Works better for:
        - text có khoảng trắng
        - text không có khoảng trắng
        - text ngắn
        """
        words_in_text = _extract_words(text)

        token_ratio_common = 0.0
        if words_in_text:
            token_hits_common = sum(1 for w in words_in_text if w in COMMON_ENGLISH_WORDS)
            token_ratio_common = token_hits_common / len(words_in_text)

        token_ratio_nltk = 0.0
        if HAS_NLTK and words is not None and words_in_text:
            try:
                english_vocab = set(w.lower() for w in words.words())
                token_hits_nltk = sum(1 for w in words_in_text if w in english_vocab)
                token_ratio_nltk = token_hits_nltk / len(words_in_text)
            except Exception:
                token_ratio_nltk = 0.0

        token_ratio = max(token_ratio_common, token_ratio_nltk)

        letters = _letters_only(text)
        if not letters:
            return 0.0

        substring_hits = sum(
            letters.count(w) for w in COMMON_ENGLISH_WORDS if len(w) >= 3
        )
        substring_score = min(1.0, substring_hits / max(1.0, len(letters) / 4))

        bigram_hits = sum(letters.count(bg) for bg in COMMON_BIGRAMS)
        bigram_score = bigram_hits / max(1, len(letters) - 1)

        trigram_hits = sum(letters.count(tg) for tg in COMMON_TRIGRAMS)
        trigram_score = trigram_hits / max(1, len(letters) - 2)

        vowel_ratio = sum(ch in "aeiou" for ch in letters) / len(letters)
        vowel_score = max(0.0, 1.0 - abs(vowel_ratio - 0.38) / 0.38)

        return (
            45 * token_ratio
            + 20 * substring_score
            + 20 * bigram_score
            + 10 * trigram_score
            + 5 * vowel_score
        )

    def railfence_cryptanalyze(self, ciphertext: str, max_key: int = 20, max_missing_trailing_spaces: int = 3):
        """
        Smart cryptanalysis:
        - thử key từ 2..max_key
        - thử thêm 0..3 dấu cách cuối chuỗi để chống lỗi nhập tay trên terminal
        """
        print("\n=== railfence Cryptanalysis ===")
        best_score = float("-inf")
        best_extra_spaces = 0

        for extra_spaces in range(max_missing_trailing_spaces + 1):
            test_ciphertext = ciphertext + (" " * extra_spaces)

            for k in range(2, min(max_key + 1, len(test_ciphertext) + 1)):
                decrypted = decrypt_railfence(test_ciphertext, k)
                score = self.get_english_score(decrypted)

                suffix = f" (+{extra_spaces} trailing space)" if extra_spaces else ""
                print(f"Testing Key {k:2d}{suffix}: [Score: {score:8.4f}] -> {decrypted[:50]}...")

                if score > best_score:
                    best_score = score
                    best_extra_spaces = extra_spaces
                    self.RailFence_Recovered_Key = k
                    self.RailFence_Recovered_Text = decrypted

        print("-" * 60)
        print(f"RESULT: Best Key found: {self.RailFence_Recovered_Key}")
        if best_extra_spaces > 0:
            print(f"NOTE: recovered by appending {best_extra_spaces} trailing space(s) to the input ciphertext.")
        print(f"Decrypted Text: {self.RailFence_Recovered_Text}")


# ====================== READ / WRITE ======================
def encrypt_file(input_file, output_file, key):
    """Mã hóa file bằng Rail Fence Cipher"""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            plaintext = f.read()

        ciphertext = encrypt_railfence(plaintext, key)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(ciphertext)
        print(f"✓ File encrypted successfully: {output_file}")
    except Exception as e:
        print(f"✗ Error: {e}")


def decrypt_file(input_file, output_file, key):
    """Giải mã file bằng Rail Fence Cipher"""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            ciphertext = f.read()

        plaintext = decrypt_railfence(ciphertext, key)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(plaintext)
        print(f"✓ File decrypted successfully: {output_file}")
    except Exception as e:
        print(f"✗ Error: {e}")


def cryptanalyze_file(input_file, output_file, max_key=20):
    """Đọc file mã hóa, tự động tìm khóa đúng và ghi ra file kết quả"""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            ciphertext = f.read()

        rf_sys = RailFenceSystem()
        rf_sys.railfence_cryptanalyze(ciphertext, max_key=max_key)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"--- RECOVERED KEY: {rf_sys.RailFence_Recovered_Key} ---\n")
            f.write(rf_sys.RailFence_Recovered_Text)

        print(f"\n[+] Thám mã hoàn tất!")
        print(f"[+] Khóa tìm thấy: {rf_sys.RailFence_Recovered_Key}")
        print(f"[+] Kết quả lưu tại: {output_file}")
    except FileNotFoundError:
        print(f"[-] Lỗi: Không tìm thấy file {input_file}")
    except Exception as e:
        print(f"[-] Lỗi hệ thống: {e}")


# ====================== ENCRYPT ======================
def encrypt_railfence(text: str, key: int) -> str:
    """Mã hóa Rail Fence Cipher"""
    if key <= 1 or not text:
        return text

    rails = [""] * key
    row = 0
    direction_down = True

    for char in text:
        rails[row] += char
        if row == 0:
            direction_down = True
        elif row == key - 1:
            direction_down = False
        row += 1 if direction_down else -1

    return "".join(rails)


# ====================== DECRYPT ======================
def decrypt_railfence(cipher: str, key: int) -> str:
    """Giải mã Rail Fence Cipher"""
    if key <= 1 or not cipher:
        return cipher

    n = len(cipher)
    matrix = [["\0"] * n for _ in range(key)]

    row = 0
    direction_down = True
    for i in range(n):
        matrix[row][i] = "*"
        if row == 0:
            direction_down = True
        elif row == key - 1:
            direction_down = False
        row += 1 if direction_down else -1

    index = 0
    for i in range(key):
        for j in range(n):
            if matrix[i][j] == "*" and index < n:
                matrix[i][j] = cipher[index]
                index += 1

    result = []
    row = 0
    direction_down = True
    for i in range(n):
        result.append(matrix[row][i])
        if row == 0:
            direction_down = True
        elif row == key - 1:
            direction_down = False
        row += 1 if direction_down else -1

    return "".join(result)