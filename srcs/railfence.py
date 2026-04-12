import nltk
from nltk.corpus import words
import ssl

# Fix lỗi SSL nếu bạn dùng MacOS hoặc mạng công ty/trường học
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Tải bộ từ điển 'words'
nltk.download('words')
class RailFenceSystem:
    def __init__(self):
        # Dữ liệu gốc
        self.Plaintext = ""
        self.RailFence_Key = 0
        
        # Kết quả mã hóa
        self.RailFence_Ciphertext = ""
        
        # Kết quả giải mã bằng khóa đúng
        self.RailFence_Decrypted_Text = ""
        
        # Kết quả thám mã (Cryptanalysis)
        self.RailFence_Recovered_Key = -1
        self.RailFence_Recovered_Text = ""
    
# ====================== CRYPTANALYSIS ======================
    def get_english_score(self, text: str) -> float:
            """Tính toán tỷ lệ phần trăm các từ có nghĩa trong văn bản"""
            english_vocab = set(w.lower() for w in words.words())
            words_in_text = text.lower().split()
            if not words_in_text:
                return 0
            
            matches = sum(1 for word in words_in_text if word in english_vocab)
            return (matches / len(words_in_text)) * 100

    def railfence_cryptanalyze(self, ciphertext: str, max_key: int = 20):
            """Thám mã tự động và lưu kết quả tốt nhất vào class"""
            print("\n=== railfence Cryptanalysis ===")
            best_score = -1
            
            for k in range(2, min(max_key + 1, len(ciphertext) + 1)):
                decrypted = decrypt_railfence(ciphertext, k)
                score = self.get_english_score(decrypted)
                
                print(f"Testing Key {k:2d}: [Score: {score:6.2f}%] -> {decrypted[:50]}...")
                
                if score > best_score:
                    best_score = score
                    self.RailFence_Recovered_Key = k
                    self.RailFence_Recovered_Text = decrypted

            print("-" * 60)
            print(f"RESULT: Best Key found: {self.RailFence_Recovered_Key}")
            print(f"Decrypted Text: {self.RailFence_Recovered_Text}")
  # ====================== read-write ====================== 
def encrypt_file(input_file, output_file, key):
    """Mã hóa file bằng Rail Fence Cipher"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            plaintext = f.read()
        
        ciphertext = encrypt_railfence(plaintext, key)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(ciphertext)
        print(f"✓ File encrypted successfully: {output_file}")
    except Exception as e:
        print(f"✗ Error: {e}")

def decrypt_file(input_file, output_file, key):
    """Giải mã file bằng Rail Fence Cipher"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            ciphertext = f.read()
        
        plaintext = decrypt_railfence(ciphertext, key)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(plaintext)
        print(f"✓ File decrypted successfully: {output_file}")
    except Exception as e:
        print(f"✗ Error: {e}")
def cryptanalyze_file(input_file, output_file, max_key=20):
    """Đọc file mã hóa, tự động tìm khóa đúng và ghi ra file kết quả"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            ciphertext = f.read()
        
        # Sử dụng class RailFenceSystem để chấm điểm ngôn ngữ
        rf_sys = RailFenceSystem()
        rf_sys.railfence_cryptanalyze(ciphertext, max_key=max_key)
        
        # Ghi nội dung đã bẻ khóa vào file mới
        with open(output_file, 'w', encoding='utf-8') as f:
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
    matrix = [['\0'] * n for _ in range(key)]
    row = 0
    direction_down = True
    for i in range(n):
        matrix[row][i] = '*'
        if row == 0:
            direction_down = True
        elif row == key - 1:
            direction_down = False
        row += 1 if direction_down else -1
    index = 0
    for i in range(key):
        for j in range(n):
            if matrix[i][j] == '*' and index < n:
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



