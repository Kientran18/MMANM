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


# ====================== CRYPTANALYSIS ======================
def cryptanalyze_railfence(ciphertext: str, max_key: int = 20):
    """Thám mã bằng cách thử tất cả các khóa"""
    print("\n=== Cryptanalysis (Brute Force) ===")
    print(f"Ciphertext: {ciphertext}")
    print("-" * 60)
    
    for k in range(2, min(max_key + 1, len(ciphertext) + 1)):
        decrypted = decrypt_railfence(ciphertext, k)
        print(f"Key = {k:2d}  →  {decrypted}")

