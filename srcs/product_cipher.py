"""
Product Cipher implementation: Caesar Cipher followed by Rail Fence Cipher.

This module follows the assignment requirement:
1. Encrypt with Caesar first
2. Encrypt the intermediate result with Rail Fence
3. Decrypt in the reverse order
4. Support cryptanalysis to recover plaintext and keys from ciphertext
"""

from __future__ import annotations

import re
from typing import Dict, List

import caesar
import railfence


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
    "hello", "world", "discover", "discovered", "flee", "once",
    "secret", "message", "cipher", "rail", "fence"
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


class ProductCipherSystem:
    """Store product cipher state and cryptanalysis results."""

    def __init__(self) -> None:
        self.Plaintext = ""
        self.Caesar_Key = 0
        self.RailFence_Key = 0
        self.Product_Ciphertext = ""
        self.Product_Decrypted_Text = ""
        self.Product_Recovered_Caesar_Key = -1
        self.Product_Recovered_RailFence_Key = -1
        self.Product_Recovered_Text = ""
        self.Product_Best_Score = float("inf")

    def product_cryptanalyze(
        self,
        ciphertext: str,
        max_rail_key: int = 20,
        top_n: int = 5
    ) -> List[Dict[str, object]]:
        """Recover likely keys and plaintext from product-cipher ciphertext."""
        candidates = brute_force_product(ciphertext, max_rail_key=max_rail_key, top_n=top_n)

        if candidates:
            best = candidates[0]
            self.Product_Recovered_Caesar_Key = int(best["caesar_key"])
            self.Product_Recovered_RailFence_Key = int(best["rail_key"])
            self.Product_Recovered_Text = str(best["plaintext"])
            self.Product_Best_Score = float(best["score"])

        return candidates


def encrypt_product(plaintext: str, caesar_key: int, rail_key: int) -> str:
    """Encrypt by Caesar first, then Rail Fence."""
    after_caesar = caesar.encrypt(plaintext, caesar_key)
    return railfence.encrypt_railfence(after_caesar, rail_key)


def decrypt_product(ciphertext: str, caesar_key: int, rail_key: int) -> str:
    """Decrypt in reverse order: Rail Fence first, then Caesar."""
    after_railfence = railfence.decrypt_railfence(ciphertext, rail_key)
    return caesar.decrypt(after_railfence, caesar_key)


def _extract_words(text: str) -> List[str]:
    return re.findall(r"[A-Za-z']+", text.lower())


def _letters_only(text: str) -> str:
    return re.sub(r"[^A-Za-z]", "", text).lower()


def _english_word_ratio(text: str) -> float:
    words = _extract_words(text)
    if not words:
        return 0.0
    hits = sum(1 for word in words if word in COMMON_ENGLISH_WORDS)
    return hits / len(words)


def _english_structure_bonus(text: str) -> float:
    words = _extract_words(text)
    token_ratio = 0.0
    if words:
        token_hits = sum(1 for w in words if w in COMMON_ENGLISH_WORDS)
        token_ratio = token_hits / len(words)

    letters = _letters_only(text)
    if not letters:
        return 0.0

    substring_hits = sum(
        letters.count(w) for w in COMMON_ENGLISH_WORDS if len(w) >= 3
    )
    substring_score = substring_hits / max(1, len(letters) / 4)

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


def score_plaintext(text: str) -> float:
    """
    Lower score = text is more likely to be valid English.
    Important:
    - luôn dùng cả unigram + bigram
    - cộng thêm English-structure bonus để phân biệt rail key tốt hơn
    """
    alpha_count = sum(1 for c in text if c.isalpha())
    if alpha_count == 0:
        return float("inf")

    unigram_score = caesar.chi_squared_test(
        caesar.analyze_frequency(text),
        caesar.standard_english_freq(),
    )

    bigram_score = caesar.chi_squared_test(
        caesar.analyze_bigram_frequency(text),
        caesar.standard_english_bigram_freq(),
    )

    if alpha_count < 20:
        score = 0.55 * unigram_score + 0.45 * bigram_score
    elif alpha_count < 100:
        score = 0.35 * unigram_score + 0.65 * bigram_score
    else:
        score = 0.25 * unigram_score + 0.75 * bigram_score

    score -= _english_word_ratio(text) * 40.0
    score -= _english_structure_bonus(text)

    return score


def brute_force_product(
    ciphertext: str,
    max_rail_key: int = 20,
    top_n: int = 5,
    max_missing_trailing_spaces: int = 3
) -> List[Dict[str, object]]:
    """
    Try rail keys and Caesar keys to recover the plaintext.
    Also tries appending 0..3 trailing spaces to reduce terminal-input errors.
    """
    if not ciphertext:
        return []

    results: List[Dict[str, object]] = []

    for extra_spaces in range(max_missing_trailing_spaces + 1):
        test_ciphertext = ciphertext + (" " * extra_spaces)
        upper_rail_key = min(max_rail_key, max(2, len(test_ciphertext) - 1))

        for rail_key in range(2, upper_rail_key + 1):
            after_rail = railfence.decrypt_railfence(test_ciphertext, rail_key)

            for caesar_key in range(26):
                plaintext = caesar.decrypt(after_rail, caesar_key)
                score = score_plaintext(plaintext)
                results.append(
                    {
                        "caesar_key": caesar_key,
                        "rail_key": rail_key,
                        "plaintext": plaintext,
                        "score": score,
                        "missing_trailing_spaces": extra_spaces,
                    }
                )

    results.sort(
        key=lambda item: (
            float(item["score"]),
            int(item["rail_key"]),
            int(item["caesar_key"]),
        )
    )
    return results[:top_n]


def cryptanalyze_product(ciphertext: str, max_rail_key: int = 20) -> Dict[str, object] | None:
    """Return the single best recovery candidate."""
    candidates = brute_force_product(ciphertext, max_rail_key=max_rail_key, top_n=1)
    return candidates[0] if candidates else None


def cryptanalyze_product_display(ciphertext: str, max_rail_key: int = 20, top_n: int = 5) -> None:
    """Display the top product-cipher recovery candidates."""
    candidates = brute_force_product(ciphertext, max_rail_key=max_rail_key, top_n=top_n)

    print("\n" + "=" * 120)
    print("PRODUCT CIPHER CRYPTANALYSIS (RAIL FENCE -> CAESAR)")
    print("=" * 120)
    print(f"Ciphertext: {ciphertext[:120]}{'...' if len(ciphertext) > 120 else ''}\n")

    if not candidates:
        print("No candidate could be recovered.")
        return

    print(f"{'Rank':<5} {'Caesar':<8} {'Rail':<6} {'Score':<14} {'Recovered Plaintext'}")
    print("-" * 120)

    for rank, candidate in enumerate(candidates, start=1):
        caesar_key = int(candidate["caesar_key"])
        rail_key = int(candidate["rail_key"])
        score = float(candidate["score"])
        plaintext = str(candidate["plaintext"])
        preview = plaintext[:80].replace("\n", " ")
        print(f"{rank:<5} {caesar_key:<8} {rail_key:<6} {score:<14.4f} {preview}{'...' if len(plaintext) > 80 else ''}")

    best = candidates[0]
    print("-" * 120)
    print(
        f"Best candidate -> Caesar key = {best['caesar_key']}, "
        f"Rail Fence key = {best['rail_key']}, score = {float(best['score']):.4f}"
    )
    if int(best.get("missing_trailing_spaces", 0)) > 0:
        print(f"NOTE: recovered by appending {best['missing_trailing_spaces']} trailing space(s) to the input ciphertext.")
    print("\nRecovered plaintext:\n")
    print(best["plaintext"])


def encrypt_file(input_file: str, output_file: str, caesar_key: int, rail_key: int) -> None:
    """Encrypt a plaintext file with the product cipher."""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            plaintext = f.read()

        ciphertext = encrypt_product(plaintext, caesar_key, rail_key)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(ciphertext)

        print(f"Product encryption successful: {output_file}")
    except FileNotFoundError:
        print(f"Error: File not found - {input_file}")
    except Exception as e:
        print(f"Error: {e}")


def decrypt_file(input_file: str, output_file: str, caesar_key: int, rail_key: int) -> None:
    """Decrypt a product-cipher file when both keys are known."""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            ciphertext = f.read()

        plaintext = decrypt_product(ciphertext, caesar_key, rail_key)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(plaintext)

        print(f"Product decryption successful: {output_file}")
    except FileNotFoundError:
        print(f"Error: File not found - {input_file}")
    except Exception as e:
        print(f"Error: {e}")


def cryptanalyze_file(input_file: str, output_file: str, max_rail_key: int = 20, top_n: int = 5) -> None:
    """Recover likely plaintext and keys from an encrypted file."""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            ciphertext = f.read()

        candidates = brute_force_product(ciphertext, max_rail_key=max_rail_key, top_n=top_n)
        if not candidates:
            print("No candidate could be recovered.")
            return

        best = candidates[0]
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("=== PRODUCT CIPHER CRYPTANALYSIS RESULT ===\n")
            f.write(f"Recovered Caesar key: {best['caesar_key']}\n")
            f.write(f"Recovered Rail Fence key: {best['rail_key']}\n")
            f.write(f"Score: {float(best['score']):.4f}\n")
            if int(best.get("missing_trailing_spaces", 0)) > 0:
                f.write(f"Recovered by appending trailing spaces: {best['missing_trailing_spaces']}\n")
            f.write("\nRecovered plaintext:\n")
            f.write(str(best["plaintext"]))
            f.write("\n\nTop candidates:\n")
            for idx, candidate in enumerate(candidates, start=1):
                f.write(
                    f"{idx}. Caesar={candidate['caesar_key']}, "
                    f"Rail={candidate['rail_key']}, "
                    f"Score={float(candidate['score']):.4f}, "
                    f"ExtraSpaces={candidate.get('missing_trailing_spaces', 0)}\n"
                )

        print(f"Product cryptanalysis result saved to: {output_file}")
    except FileNotFoundError:
        print(f"Error: File not found - {input_file}")
    except Exception as e:
        print(f"Error: {e}")