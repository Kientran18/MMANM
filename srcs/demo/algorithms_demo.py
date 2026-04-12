"""
Demo: Hai Thuật Toán Brute Force Attack trên Caesar Cipher
1. Duyệt Cạn (Exhaustive Search)
2. Phân tích Tần suất (Frequency Analysis)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from caesar import (
    encrypt,
    brute_force_exhaustive,
    brute_force_exhaustive_display,
    brute_force_frequency_analysis,
    brute_force_frequency_analysis_display
)


def demo_1_exhaustive_search():
    """
    DEMO 1: THUẬT TOÁN DUYỆT CẠN (EXHAUSTIVE SEARCH)
    
    Cách hoạt động:
    - Thử tất cả 26 khóa có thể
    - Hiển thị từng kết quả giải mã
    - Người dùng tự xác định khóa nào là chính xác
    
    Ưu điểm:
    - Đơn giản, dễ hiểu
    - Chắc chắn sẽ tìm được khóa đúng
    - Tốt cho text ngắn hoặc khi cần xem tất cả khả năng
    
    Nhược điểm:
    - Yêu cầu người dùng phải kiểm tra từng kết quả
    - Không tự động xác định khóa chính xác
    """
    
    print("\n" + "=" * 80)
    print("DEMO 1: THUẬT TOÁN DUYỆT CẠN (EXHAUSTIVE SEARCH)")
    print("=" * 80)
    
    # Kịch bản: Người ta gửi cho bạn một đoạn tin nhắn mã hóa bằng Caesar cipher
    # Bạn không biết khóa
    
    original = "Secret Message"
    secret_key = 7
    encrypted = encrypt(original, secret_key)
    
    print(f"\n📨 Bạn nhận được: {encrypted}")
    print(f"❓ Bạn không biết khóa là bao nhiêu...\n")
    
    print("🔍 Sử dụng DUYỆT CẠN - Thử tất cả 26 khóa:\n")
    
    results = brute_force_exhaustive(encrypted)
    print(f"{'Khóa':<6} {'Kết quả giải mã':<40}")
    print("-" * 50)
    
    for key, plaintext in results:
        marker = " ← ✓ ĐÂY LÀ TIN NHẮN GỐCC!" if key == secret_key else ""
        print(f"{key:<6} {plaintext:<40}{marker}")
    
    print("-" * 50)
    print(f"\n✓ Kết luận: Khóa là {secret_key}")
    print("⚠️  Lưu ý: Bạn phải tự nhận ra đó là tin nhắn hợp lý (~reading)")


def demo_2_frequency_analysis():
    """
    DEMO 2: THUẬT TOÁN PHÂN TÍCH TẦN SUẤT (FREQUENCY ANALYSIS)
    
    Cách hoạt động:
    1. Phân tích tần suất ký tự trong văn bản mã hóa
    2. So sánh với tần suất tiêu chuẩn của tiếng Anh (e, t, a, o...)
    3. Dùng công thức Chi-Squared để tính độ phù hợp
    4. Khóa có chi-squared thấp nhất = khóa đúng
    
    Ưu điểm:
    - TỰ ĐỘNG xác định khóa (không cần người kiểm tra)
    - Hiệu quả với text dài (>100 ký tự)
    - Dựa trên toán học, không phải "đoán"
    
    Nhược điểm:
    - Yêu cầu text đủ dài để phân tích
    - Không hiệu quả với text ngắn hoặc text không phải tiếng Anh
    """
    
    print("\n" + "=" * 80)
    print("DEMO 2: THUẬT TOÁN PHÂN TÍCH TẦN SUẤT (FREQUENCY ANALYSIS)")
    print("=" * 80)
    
    # Kịch bản: Một đoạn tin nhắn dài (để tần suất đủ rõ ràng)
    original = """The Caesar cipher is one of the simplest and most widely known 
    encryption techniques. It is a type of substitution cipher in which each letter in 
    the plaintext is replaced by a letter some fixed number of positions down the alphabet. 
    The method is named after Julius Caesar who used it to communicate with his generals."""
    
    secret_key = 13
    encrypted = encrypt(original, secret_key)
    
    print(f"\n📨 Bạn nhận được: {encrypted[:100]}...")
    print(f"❓ Bạn không biết khóa là bao nhiêu...\n")
    
    print("🔍 Sử dụng PHÂN TÍCH TẦN SUẤT - Tính chi-squared cho 26 khóa:\n")
    
    # Hiển thị kết quả
    brute_force_frequency_analysis_display(encrypted, show_top=5)
    
    print("💡 Giải thích:")
    print("   - Chi-Squared càng thấp = tần suất ký tự càng gần với tiêu chuẩn tiếng Anh")
    print("   - Khóa có chi-squared thấp nhất là khóa hợp lệ nhất")
    print("   - Không cần kiểm tra thủ công, máy tự động xác định được!")


def demo_3_comparison():
    """
    DEMO 3: SO SÁNH 2 THUẬT TOÁN
    """
    
    print("\n" + "=" * 80)
    print("DEMO 3: SO SÁNH 2 THUẬT TOÁN")
    print("=" * 80)
    
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                   DUYỆT CẠN vs PHÂN TÍCH TẦN SUẤT                         ║
╠════════════════════╦════════════════════╦════════════════════════════════╣
║ TIÊU CHÍ           ║ DUYỆT CẠN          ║ PHÂN TÍCH TẦN SUẤT             ║
╠════════════════════╬════════════════════╬════════════════════════════════╣
║ Cách hoạt động     ║ Thử tất cả 26 khóa ║ Phân tích + Chi-Squared test   ║
╠════════════════════╬════════════════════╬════════════════════════════════╣
║ Yêu cầu người      ║ CÓ - Phải kiểm tra ║ KHÔNG - Tự động xác định      ║
║ kiểm tra           ║ từng kết quả       ║                                ║
╠════════════════════╬════════════════════╬════════════════════════════════╣
║ Độ phức tạp        ║ O(26n) = O(n)      ║ O(26n) = O(n)                  ║
╠════════════════════╬════════════════════╬════════════════════════════════╣
║ Kích thước text    ║ Tốt cho text ngắn  ║ Tốt cho text dài (>100 ký tự) ║
╠════════════════════╬════════════════════╬════════════════════════════════╣
║ Hiệu quả          ║ 100% (nếu đoán     ║ ~95% (phụ thuộc vào text)      ║
║                   ║ đúng khóa)         ║                                ║
╠════════════════════╬════════════════════╬════════════════════════════════╣
║ VÍ DỤ HỢP LÝ       ║ • Tin nhắn ngắn    ║ • Email dài                    ║
║                   ║ • Kiểm tra tay     ║ • Văn bản sách                ║
║                   ║ • Học tập          ║ • Tấn công thực tế             ║
╚════════════════════╩════════════════════╩════════════════════════════════╝
    """)
    
    print("✅ KẾT LUẬN:")
    print("   • Text NGẮN (<100 ký tự) → Dùng DUYỆT CẠN")
    print("   • Text DÀI (>100 ký tự)  → Dùng PHÂN TÍCH TẦN SUẤT")
    print("   • Cả hai phương pháp đều có thể thử trong main.py!")


def main():
    """Chạy tất cả các demo."""
    print("\n" + "=" * 80)
    print("HAI THUẬT TOÁN BRUTE FORCE ATTACK TRÊN CAESAR CIPHER")
    print("=" * 80)
    
    demo_1_exhaustive_search()
    demo_2_frequency_analysis()
    demo_3_comparison()
    
    print("\n" + "=" * 80)
    print("HÃYCHẠY: python main.py")
    print("  Để sử dụng cả 2 thuật toán trong menu tương tác!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
