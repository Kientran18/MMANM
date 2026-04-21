from __future__ import annotations

import io
import traceback
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

import caesar
import railfence
import product_cipher


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PLAINTEXT_PATH = DATA_DIR / "plaintext.txt"

TOTAL = 0
PASSED = 0
FAILED = 0


def line(char: str = "-", n: int = 90) -> str:
    return char * n


def print_header(title: str) -> None:
    print("\n" + line("="))
    print(title)
    print(line("="))


def print_subheader(title: str) -> None:
    print("\n" + line("-"))
    print(title)
    print(line("-"))


def short_text(value, limit: int = 220) -> str:
    text = str(value)
    text = text.replace("\n", "\\n")
    if len(text) > limit:
        return text[:limit] + "... [truncated]"
    return text


def show_case(name: str, inp=None, expected=None, actual=None, detail: str = "") -> None:
    print(f"Test    : {name}")
    if inp is not None:
        print(f"Input   : {short_text(inp)}")
    if expected is not None:
        print(f"Expected: {short_text(expected)}")
    if actual is not None:
        print(f"Actual  : {short_text(actual)}")
    if detail:
        print(f"Detail  : {detail}")


def pass_test(name: str, inp=None, expected=None, actual=None, detail: str = "") -> None:
    global TOTAL, PASSED
    TOTAL += 1
    PASSED += 1
    show_case(name, inp, expected, actual, detail)
    print("Result  : PASS")
    print(line())


def fail_test(name: str, inp=None, expected=None, actual=None, detail: str = "") -> None:
    global TOTAL, FAILED
    TOTAL += 1
    FAILED += 1
    show_case(name, inp, expected, actual, detail)
    print("Result  : FAIL")
    print(line())


def assert_equal(name: str, actual, expected, inp=None, detail: str = "") -> None:
    if actual == expected:
        pass_test(name, inp=inp, expected=expected, actual=actual, detail=detail)
    else:
        fail_test(name, inp=inp, expected=expected, actual=actual, detail=detail)


def assert_true(name: str, condition: bool, inp=None, actual=None, expected=None, detail: str = "") -> None:
    if condition:
        pass_test(name, inp=inp, expected=expected, actual=actual, detail=detail)
    else:
        fail_test(name, inp=inp, expected=expected, actual=actual, detail=detail)


def capture_output(func, *args, **kwargs) -> str:
    buf = io.StringIO()
    with redirect_stdout(buf):
        func(*args, **kwargs)
    return buf.getvalue()


def safe_run(group_name: str, fn) -> None:
    try:
        fn()
    except Exception:
        fail_test(
            group_name,
            detail=traceback.format_exc(),
        )


def load_plaintext() -> str:
    if not PLAINTEXT_PATH.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {PLAINTEXT_PATH}")
    return PLAINTEXT_PATH.read_text(encoding="utf-8")


def ensure_nltk_words() -> None:
    try:
        import nltk
        from nltk.corpus import words

        try:
            _ = words.words()[:5]
        except LookupError:
            nltk.download("words", quiet=True)
    except Exception:
        pass


# =========================================================
# CAESAR TESTS
# =========================================================
def test_caesar_functions() -> None:
    print_header("CAESAR TESTS")

    sample_plain = "Hello World 123!"
    sample_key = 3
    sample_cipher = "Khoor Zruog 123!"

    print_subheader("Short-string tests")

    actual_cipher = caesar.encrypt(sample_plain, sample_key)
    assert_equal(
        "caesar.encrypt short string",
        actual_cipher,
        sample_cipher,
        inp=f"plaintext={sample_plain}, key={sample_key}",
    )

    actual_plain = caesar.decrypt(sample_cipher, sample_key)
    assert_equal(
        "caesar.decrypt short string",
        actual_plain,
        sample_plain,
        inp=f"ciphertext={sample_cipher}, key={sample_key}",
    )

    results = caesar.brute_force_exhaustive(sample_cipher)
    assert_equal(
        "caesar.brute_force_exhaustive returns 26 cases",
        len(results),
        26,
        inp=f"ciphertext={sample_cipher}",
    )

    contains_correct = any(k == sample_key and pt == sample_plain for k, pt in results)
    assert_true(
        "caesar.brute_force_exhaustive contains correct key/plaintext",
        contains_correct,
        inp=f"ciphertext={sample_cipher}",
        expected="a pair (3, 'Hello World 123!') exists",
        actual=str(results[:5]) + " ...",
    )

    out = capture_output(caesar.brute_force_exhaustive_display, sample_cipher)
    assert_true(
        "caesar.brute_force_exhaustive_display prints expected content",
        "EXHAUSTIVE SEARCH" in out and sample_plain in out,
        inp=f"ciphertext={sample_cipher}",
        expected="output contains heading and correct plaintext",
        actual=out,
    )

    freq = caesar.analyze_frequency("AaBbA!")
    assert_equal(
        "caesar.analyze_frequency",
        freq,
        {"a": 3, "b": 2},
        inp="AaBbA!",
    )

    bigram = caesar.analyze_bigram_frequency("ABABA!")
    assert_equal(
        "caesar.analyze_bigram_frequency",
        bigram,
        {"ab": 2, "ba": 2},
        inp="ABABA!",
    )

    std_freq = caesar.standard_english_freq()
    assert_equal(
        "caesar.standard_english_freq has 26 letters",
        len(std_freq),
        26,
    )

    std_bigram = caesar.standard_english_bigram_freq()
    assert_true(
        "caesar.standard_english_bigram_freq not empty",
        len(std_bigram) > 0,
        actual=f"len={len(std_bigram)}",
        expected="len > 0",
    )

    english_score = caesar.chi_squared_test(
        caesar.analyze_frequency("this is a simple english sentence"),
        caesar.standard_english_freq(),
    )
    nonsense_score = caesar.chi_squared_test(
        caesar.analyze_frequency("xqz qzx qzz xyy"),
        caesar.standard_english_freq(),
    )
    assert_true(
        "caesar.chi_squared_test prefers English-like text",
        english_score < nonsense_score,
        expected="english_score < nonsense_score",
        actual=f"english_score={english_score}, nonsense_score={nonsense_score}",
    )

    rec1 = caesar.recommend_analysis_method("HELLO")
    rec2 = caesar.recommend_analysis_method("A" * 30)
    rec3 = caesar.recommend_analysis_method("A" * 70)
    rec4 = caesar.recommend_analysis_method("A" * 150)

    assert_equal("caesar.recommend_analysis_method short", rec1["method"], "Exhaustive Search", inp="HELLO")
    assert_equal("caesar.recommend_analysis_method 30 chars", rec2["method"], "Exhaustive + Frequency Analysis", inp="A" * 30)
    assert_equal("caesar.recommend_analysis_method 70 chars", rec3["method"], "Unigram Frequency Analysis", inp="A" * 70)
    assert_equal("caesar.recommend_analysis_method 150 chars", rec4["method"], "Unigram + Bigram Analysis", inp="A" * 150)

    print_subheader("Plaintext-file tests")

    plaintext = load_plaintext()
    key = 5
    ciphertext = caesar.encrypt(plaintext, key)

    best_uni = caesar.brute_force_frequency_analysis(ciphertext)
    assert_equal(
        "caesar.brute_force_frequency_analysis key",
        best_uni[0],
        key,
        inp=f"ciphertext from plaintext.txt with key={key}",
    )
    assert_equal(
        "caesar.brute_force_frequency_analysis plaintext",
        best_uni[1],
        plaintext,
        inp=f"ciphertext from plaintext.txt with key={key}",
    )

    top_uni = caesar.brute_force_frequency_analysis_top_n(ciphertext, n=5)
    assert_true(
        "caesar.brute_force_frequency_analysis_top_n contains correct key",
        any(k == key for k, _, _ in top_uni),
        inp=f"ciphertext from plaintext.txt with key={key}",
        expected=f"key {key} appears in top 5",
        actual=str([(k, round(score, 4)) for k, _, score in top_uni]),
    )

    out_uni = capture_output(caesar.brute_force_frequency_analysis_display, ciphertext, 5)
    assert_true(
        "caesar.brute_force_frequency_analysis_display prints expected content",
        "FREQUENCY ANALYSIS RESULTS" in out_uni and f"Best key: {key}" in out_uni,
        inp=f"ciphertext from plaintext.txt with key={key}",
        expected="output contains heading and best key",
        actual=out_uni,
    )

    best_bigram = caesar.brute_force_frequency_analysis_bigram(ciphertext)
    assert_equal(
        "caesar.brute_force_frequency_analysis_bigram key",
        best_bigram[0],
        key,
        inp=f"ciphertext from plaintext.txt with key={key}",
    )
    assert_equal(
        "caesar.brute_force_frequency_analysis_bigram plaintext",
        best_bigram[1],
        plaintext,
        inp=f"ciphertext from plaintext.txt with key={key}",
    )

    top_bigram = caesar.brute_force_frequency_analysis_bigram_top_n(ciphertext, n=5)
    assert_true(
        "caesar.brute_force_frequency_analysis_bigram_top_n contains correct key",
        any(k == key for k, _, _ in top_bigram),
        inp=f"ciphertext from plaintext.txt with key={key}",
        expected=f"key {key} appears in top 5",
        actual=str([(k, round(score, 4)) for k, _, score in top_bigram]),
    )

    out_bigram = capture_output(caesar.brute_force_frequency_analysis_bigram_display, ciphertext, 5)
    assert_true(
        "caesar.brute_force_frequency_analysis_bigram_display prints expected content",
        "UNIGRAM + BIGRAM" in out_bigram and f"Key found: {key}" in out_bigram,
        inp=f"ciphertext from plaintext.txt with key={key}",
        expected="output contains heading and found key",
        actual=out_bigram,
    )

    print_subheader("File-function tests")

    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        in_file = tmpdir / "plain.txt"
        cipher_file = tmpdir / "cipher.txt"
        decrypted_file = tmpdir / "decrypt.txt"

        in_file.write_text(plaintext, encoding="utf-8")

        encrypt_out = capture_output(caesar.encrypt_file, str(in_file), str(cipher_file), key)
        assert_true(
            "caesar.encrypt_file creates output file",
            cipher_file.exists(),
            inp=f"input={in_file}, output={cipher_file}, key={key}",
            expected="cipher file exists",
            actual=encrypt_out,
        )

        decrypt_out = capture_output(caesar.decrypt_file, str(cipher_file), str(decrypted_file), key)
        assert_true(
            "caesar.decrypt_file creates output file",
            decrypted_file.exists(),
            inp=f"input={cipher_file}, output={decrypted_file}, key={key}",
            expected="decrypt file exists",
            actual=decrypt_out,
        )

        if cipher_file.exists() and decrypted_file.exists():
            roundtrip = decrypted_file.read_text(encoding="utf-8")
            assert_equal(
                "caesar file round-trip",
                roundtrip,
                plaintext,
                inp=f"plaintext.txt -> encrypt_file -> decrypt_file with key={key}",
            )

    print_subheader("Caesar file cryptanalysis tests")

    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        in_file = tmpdir / "plain.txt"
        cipher_file = tmpdir / "cipher.txt"
        exhaustive_solution_file = tmpdir / "caesar_exhaustive_solution.txt"
        frequency_solution_file = tmpdir / "caesar_frequency_solution.txt"

        crypt_key = 3
        in_file.write_text(plaintext, encoding="utf-8")

        encrypt_out = capture_output(caesar.encrypt_file, str(in_file), str(cipher_file), crypt_key)
        assert_true(
            "caesar.encrypt_file for cryptanalysis creates ciphertext file",
            cipher_file.exists(),
            inp=f"input={in_file}, output={cipher_file}, key={crypt_key}",
            expected="cipher file exists",
            actual=encrypt_out,
        )

        exhaustive_out = capture_output(
            caesar.cryptanalyze_file_exhaustive,
            str(cipher_file),
            str(exhaustive_solution_file),
        )

        assert_true(
            "caesar.cryptanalyze_file_exhaustive creates solution file",
            exhaustive_solution_file.exists(),
            inp=f"input={cipher_file}, output={exhaustive_solution_file}",
            expected="solution file exists",
            actual=exhaustive_out,
        )

        if exhaustive_solution_file.exists():
            exhaustive_text = exhaustive_solution_file.read_text(encoding="utf-8")

            assert_true(
                "caesar.cryptanalyze_file_exhaustive output contains heading",
                "=== CAESAR CRYPTANALYSIS RESULT (EXHAUSTIVE SEARCH) ===" in exhaustive_text,
                expected="heading exists",
                actual=exhaustive_text,
            )

            assert_true(
                "caesar.cryptanalyze_file_exhaustive recovers key",
                "Best key (ranked by chi-squared): 3" in exhaustive_text,
                expected="Best key (ranked by chi-squared): 3",
                actual=exhaustive_text,
            )

            assert_true(
                "caesar.cryptanalyze_file_exhaustive contains recovered plaintext",
                plaintext[:200] in exhaustive_text,
                expected="plaintext preview appears in solution file",
                actual=exhaustive_text,
            )

            assert_true(
                "caesar.cryptanalyze_file_exhaustive terminal output shows recovered key",
                "Recovered key: 3" in exhaustive_out,
                expected="Recovered key: 3",
                actual=exhaustive_out,
            )

        frequency_out = capture_output(
            caesar.cryptanalyze_file_frequency,
            str(cipher_file),
            str(frequency_solution_file),
            5,
        )

        assert_true(
            "caesar.cryptanalyze_file_frequency creates solution file",
            frequency_solution_file.exists(),
            inp=f"input={cipher_file}, output={frequency_solution_file}, top_n=5",
            expected="solution file exists",
            actual=frequency_out,
        )

        if frequency_solution_file.exists():
            frequency_text = frequency_solution_file.read_text(encoding="utf-8")

            assert_true(
                "caesar.cryptanalyze_file_frequency output contains heading",
                "=== CAESAR CRYPTANALYSIS RESULT (FREQUENCY ANALYSIS) ===" in frequency_text,
                expected="heading exists",
                actual=frequency_text,
            )

            assert_true(
                "caesar.cryptanalyze_file_frequency recovers key",
                "Recovered key: 3" in frequency_text,
                expected="Recovered key: 3",
                actual=frequency_text,
            )

            assert_true(
                "caesar.cryptanalyze_file_frequency contains recommended method",
                "Recommended method:" in frequency_text and "Method used:" in frequency_text,
                expected="both Recommended method and Method used appear",
                actual=frequency_text,
            )

            assert_true(
                "caesar.cryptanalyze_file_frequency contains recovered plaintext",
                plaintext[:200] in frequency_text,
                expected="plaintext preview appears in solution file",
                actual=frequency_text,
            )

            assert_true(
                "caesar.cryptanalyze_file_frequency terminal output shows recovered key",
                "Recovered key: 3" in frequency_out,
                expected="Recovered key: 3",
                actual=frequency_out,
            )


# =========================================================
# RAIL FENCE TESTS
# =========================================================
def test_railfence_functions() -> None:
    print_header("RAIL FENCE TESTS")

    ensure_nltk_words()
    rf_sys = railfence.RailFenceSystem()

    sample_plain = "WEAREDISCOVEREDFLEEATONCE"
    sample_key = 3
    sample_cipher = "WECRLTEERDSOEEFEAOCAIVDEN"

    print_subheader("Short-string tests")

    actual_cipher = railfence.encrypt_railfence(sample_plain, sample_key)
    assert_equal(
        "railfence.encrypt_railfence short string",
        actual_cipher,
        sample_cipher,
        inp=f"plaintext={sample_plain}, key={sample_key}",
    )

    actual_plain = railfence.decrypt_railfence(sample_cipher, sample_key)
    assert_equal(
        "railfence.decrypt_railfence short string",
        actual_plain,
        sample_plain,
        inp=f"ciphertext={sample_cipher}, key={sample_key}",
    )

    assert_equal(
        "railfence.encrypt_railfence key=1",
        railfence.encrypt_railfence("HELLO", 1),
        "HELLO",
        inp="plaintext=HELLO, key=1",
    )

    assert_equal(
        "railfence.decrypt_railfence empty string",
        railfence.decrypt_railfence("", 4),
        "",
        inp="ciphertext='', key=4",
    )

    good_score = rf_sys.get_english_score("this is a simple english sentence")
    bad_score = rf_sys.get_english_score("xqz qzx qzz xyy")
    assert_true(
        "RailFenceSystem.get_english_score prefers English text",
        good_score > bad_score,
        expected="good_score > bad_score",
        actual=f"good_score={good_score}, bad_score={bad_score}",
    )

    print_subheader("Plaintext-file tests")

    plaintext = load_plaintext()
    key = 4
    ciphertext = railfence.encrypt_railfence(plaintext, key)
    recovered = railfence.decrypt_railfence(ciphertext, key)

    assert_equal(
        "railfence long plaintext round-trip",
        recovered,
        plaintext,
        inp=f"plaintext.txt with key={key}",
    )

    out = capture_output(rf_sys.railfence_cryptanalyze, ciphertext, 20)
    assert_equal(
        "RailFenceSystem.railfence_cryptanalyze key",
        rf_sys.RailFence_Recovered_Key,
        key,
        inp=f"ciphertext from plaintext.txt with key={key}",
    )
    assert_equal(
        "RailFenceSystem.railfence_cryptanalyze plaintext",
        rf_sys.RailFence_Recovered_Text,
        plaintext,
        inp=f"ciphertext from plaintext.txt with key={key}",
    )
    assert_true(
        "RailFenceSystem.railfence_cryptanalyze prints expected content",
        "Best Key found" in out or "RESULT:" in out,
        inp=f"ciphertext from plaintext.txt with key={key}",
        expected="output contains result section",
        actual=out,
    )

    print_subheader("File-function tests")

    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        in_file = tmpdir / "plain.txt"
        cipher_file = tmpdir / "cipher.txt"
        decrypt_file = tmpdir / "decrypt.txt"
        solution_file = tmpdir / "solution.txt"

        in_file.write_text(plaintext, encoding="utf-8")

        encrypt_out = capture_output(railfence.encrypt_file, str(in_file), str(cipher_file), key)
        assert_true(
            "railfence.encrypt_file creates output file",
            cipher_file.exists(),
            inp=f"input={in_file}, output={cipher_file}, key={key}",
            expected="cipher file exists",
            actual=encrypt_out,
        )

        decrypt_out = capture_output(railfence.decrypt_file, str(cipher_file), str(decrypt_file), key)
        assert_true(
            "railfence.decrypt_file creates output file",
            decrypt_file.exists(),
            inp=f"input={cipher_file}, output={decrypt_file}, key={key}",
            expected="decrypt file exists",
            actual=decrypt_out,
        )

        if decrypt_file.exists():
            roundtrip = decrypt_file.read_text(encoding="utf-8")
            assert_equal(
                "railfence file round-trip",
                roundtrip,
                plaintext,
                inp=f"plaintext.txt -> encrypt_file -> decrypt_file with key={key}",
            )

        crypt_out = capture_output(railfence.cryptanalyze_file, str(cipher_file), str(solution_file), 20)
        assert_true(
            "railfence.cryptanalyze_file creates output file",
            solution_file.exists(),
            inp=f"input={cipher_file}, output={solution_file}",
            expected="solution file exists",
            actual=crypt_out,
        )

        if solution_file.exists():
            solution_text = solution_file.read_text(encoding="utf-8")
            assert_true(
                "railfence.cryptanalyze_file contains recovered key",
                f"--- RECOVERED KEY: {key} ---" in solution_text,
                expected=f"--- RECOVERED KEY: {key} --- appears",
                actual=solution_text,
            )
            assert_true(
                "railfence.cryptanalyze_file contains plaintext",
                plaintext[:200] in solution_text,
                expected="plaintext preview appears in solution file",
                actual=solution_text,
            )


# =========================================================
# PRODUCT CIPHER TESTS
# =========================================================
def test_product_cipher_functions() -> None:
    print_header("PRODUCT CIPHER TESTS")

    sample_plain = "HELLO"
    caesar_key = 3
    rail_key = 2
    sample_cipher = "KORHO"

    print_subheader("Short-string tests")

    actual_cipher = product_cipher.encrypt_product(sample_plain, caesar_key, rail_key)
    assert_equal(
        "product_cipher.encrypt_product short string",
        actual_cipher,
        sample_cipher,
        inp=f"plaintext={sample_plain}, caesar_key={caesar_key}, rail_key={rail_key}",
    )

    actual_plain = product_cipher.decrypt_product(sample_cipher, caesar_key, rail_key)
    assert_equal(
        "product_cipher.decrypt_product short string",
        actual_plain,
        sample_plain,
        inp=f"ciphertext={sample_cipher}, caesar_key={caesar_key}, rail_key={rail_key}",
    )

    words = product_cipher._extract_words("Hello, WORLD! It's me.")
    assert_equal(
        "product_cipher._extract_words",
        words,
        ["hello", "world", "it's", "me"],
        inp="Hello, WORLD! It's me.",
    )

    ratio_good = product_cipher._english_word_ratio("the and of to in")
    ratio_bad = product_cipher._english_word_ratio("xqz qzx qzz")
    assert_true(
        "product_cipher._english_word_ratio prefers English text",
        ratio_good > ratio_bad,
        expected="ratio_good > ratio_bad",
        actual=f"ratio_good={ratio_good}, ratio_bad={ratio_bad}",
    )

    score_good = product_cipher.score_plaintext("this is a simple english sentence with the and of to in")
    score_bad = product_cipher.score_plaintext("xqz qzx qzz xyy qzx")
    assert_true(
        "product_cipher.score_plaintext prefers English text",
        score_good < score_bad,
        expected="score_good < score_bad",
        actual=f"score_good={score_good}, score_bad={score_bad}",
    )

    print_subheader("Plaintext-file tests")

    plaintext = load_plaintext()
    ck = 3
    rk = 4
    ciphertext = product_cipher.encrypt_product(plaintext, ck, rk)
    recovered = product_cipher.decrypt_product(ciphertext, ck, rk)

    assert_equal(
        "product_cipher long plaintext round-trip",
        recovered,
        plaintext,
        inp=f"plaintext.txt with caesar_key={ck}, rail_key={rk}",
    )

    candidates = product_cipher.brute_force_product(ciphertext, max_rail_key=10, top_n=5)
    assert_true(
        "product_cipher.brute_force_product returns candidates",
        len(candidates) > 0,
        inp=f"ciphertext from plaintext.txt with caesar_key={ck}, rail_key={rk}",
        expected="len(candidates) > 0",
        actual=f"len={len(candidates)}",
    )
    if candidates:
        best = candidates[0]
        assert_equal(
            "product_cipher.brute_force_product Caesar key",
            int(best["caesar_key"]),
            ck,
            inp="best candidate",
        )
        assert_equal(
            "product_cipher.brute_force_product Rail key",
            int(best["rail_key"]),
            rk,
            inp="best candidate",
        )
        assert_equal(
            "product_cipher.brute_force_product plaintext",
            str(best["plaintext"]),
            plaintext,
            inp="best candidate",
        )

    best_single = product_cipher.cryptanalyze_product(ciphertext, max_rail_key=10)
    assert_true(
        "product_cipher.cryptanalyze_product returns result",
        best_single is not None,
        inp=f"ciphertext from plaintext.txt with caesar_key={ck}, rail_key={rk}",
        expected="not None",
        actual=best_single,
    )
    if best_single is not None:
        assert_equal(
            "product_cipher.cryptanalyze_product Caesar key",
            int(best_single["caesar_key"]),
            ck,
            inp="best_single",
        )
        assert_equal(
            "product_cipher.cryptanalyze_product Rail key",
            int(best_single["rail_key"]),
            rk,
            inp="best_single",
        )
        assert_equal(
            "product_cipher.cryptanalyze_product plaintext",
            str(best_single["plaintext"]),
            plaintext,
            inp="best_single",
        )

    out = capture_output(product_cipher.cryptanalyze_product_display, ciphertext, 10, 5)
    assert_true(
        "product_cipher.cryptanalyze_product_display prints expected content",
        "PRODUCT CIPHER CRYPTANALYSIS" in out and "Best candidate" in out,
        inp=f"ciphertext from plaintext.txt with caesar_key={ck}, rail_key={rk}",
        expected="output contains heading and best candidate line",
        actual=out,
    )

    pc_sys = product_cipher.ProductCipherSystem()
    sys_candidates = pc_sys.product_cryptanalyze(ciphertext, max_rail_key=10, top_n=5)

    assert_true(
        "ProductCipherSystem.product_cryptanalyze returns candidates",
        len(sys_candidates) > 0,
        expected="len(sys_candidates) > 0",
        actual=f"len={len(sys_candidates)}",
    )
    assert_equal(
        "ProductCipherSystem recovered Caesar key",
        pc_sys.Product_Recovered_Caesar_Key,
        ck,
    )
    assert_equal(
        "ProductCipherSystem recovered Rail key",
        pc_sys.Product_Recovered_RailFence_Key,
        rk,
    )
    assert_equal(
        "ProductCipherSystem recovered plaintext",
        pc_sys.Product_Recovered_Text,
        plaintext,
    )

    print_subheader("File-function tests")

    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        in_file = tmpdir / "plain.txt"
        cipher_file = tmpdir / "cipher.txt"
        decrypt_file = tmpdir / "decrypt.txt"
        solution_file = tmpdir / "solution.txt"

        in_file.write_text(plaintext, encoding="utf-8")

        encrypt_out = capture_output(product_cipher.encrypt_file, str(in_file), str(cipher_file), ck, rk)
        assert_true(
            "product_cipher.encrypt_file creates output file",
            cipher_file.exists(),
            inp=f"input={in_file}, output={cipher_file}, caesar_key={ck}, rail_key={rk}",
            expected="cipher file exists",
            actual=encrypt_out,
        )

        decrypt_out = capture_output(product_cipher.decrypt_file, str(cipher_file), str(decrypt_file), ck, rk)
        assert_true(
            "product_cipher.decrypt_file creates output file",
            decrypt_file.exists(),
            inp=f"input={cipher_file}, output={decrypt_file}, caesar_key={ck}, rail_key={rk}",
            expected="decrypt file exists",
            actual=decrypt_out,
        )

        if decrypt_file.exists():
            roundtrip = decrypt_file.read_text(encoding="utf-8")
            assert_equal(
                "product_cipher file round-trip",
                roundtrip,
                plaintext,
                inp=f"plaintext.txt -> encrypt_file -> decrypt_file with caesar_key={ck}, rail_key={rk}",
            )

        crypt_out = capture_output(product_cipher.cryptanalyze_file, str(cipher_file), str(solution_file), 10, 5)
        assert_true(
            "product_cipher.cryptanalyze_file creates output file",
            solution_file.exists(),
            inp=f"input={cipher_file}, output={solution_file}",
            expected="solution file exists",
            actual=crypt_out,
        )

        if solution_file.exists():
            solution_text = solution_file.read_text(encoding="utf-8")
            assert_true(
                "product_cipher.cryptanalyze_file contains recovered Caesar key",
                f"Recovered Caesar key: {ck}" in solution_text,
                expected=f"Recovered Caesar key: {ck}",
                actual=solution_text,
            )
            assert_true(
                "product_cipher.cryptanalyze_file contains recovered Rail key",
                f"Recovered Rail Fence key: {rk}" in solution_text,
                expected=f"Recovered Rail Fence key: {rk}",
                actual=solution_text,
            )
            assert_true(
                "product_cipher.cryptanalyze_file contains plaintext",
                plaintext[:200] in solution_text,
                expected="plaintext preview appears in solution file",
                actual=solution_text,
            )


def print_summary() -> None:
    print("\n" + line("="))
    print("TEST SUMMARY")
    print(line("="))
    print(f"TOTAL : {TOTAL}")
    print(f"PASS  : {PASSED}")
    print(f"FAIL  : {FAILED}")


def main() -> None:
    print_header("START RUN TESTS")

    if not PLAINTEXT_PATH.exists():
        fail_test("Load plaintext", detail=f"Không tìm thấy file {PLAINTEXT_PATH}")
        print_summary()
        return

    safe_run("Caesar test group", test_caesar_functions)
    safe_run("Rail Fence test group", test_railfence_functions)
    safe_run("Product Cipher test group", test_product_cipher_functions)

    print_summary()


if __name__ == "__main__":
    main()