import os
import importlib

# === CẤU HÌNH: ĐIỀN TÊN ẢNH BẠN MUỐN TEST VÀO ĐÂY ===
TEN_FILE_ANH = "demo.png"  # <-- Đổi tên file ở đây
# ====================================================

def chay_demo():
    # 1. Kiểm tra file ảnh có tồn tại không
    if not os.path.exists(TEN_FILE_ANH):
        print(f"❌ Lỗi: Không tìm thấy file '{TEN_FILE_ANH}'")
        print("--> Bạn nhớ chép ảnh vào cùng thư mục code nhé!")
        return

    # 2. Import 3 "trợ thủ" (đảm bảo file 1, 2, 3 không bị lỗi)
    try:
        ocr_mod = importlib.import_module("ocr")
        filter_mod = importlib.import_module("filter")
        search_mod = importlib.import_module("search")
    except ImportError as e:
        print(f"❌ Lỗi: Thiếu file module! {e}")
        return

    print(f"\n🚀 BẮT ĐẦU DEMO VỚI ẢNH: {TEN_FILE_ANH}\n")

    # --- BƯỚC 1: ĐỌC ẢNH (OCR) ---
    print("--- BƯỚC 1: ĐỌC ẢNH (OCR) ---")
    raw_text = ocr_mod.extract_text_from_image(TEN_FILE_ANH)
    print(f"📄 Kết quả đọc: {raw_text}")
    
    if not raw_text:
        print("⛔ Dừng: Không đọc được chữ nào.")
        return

    # --- BƯỚC 2: PHÂN TÍCH Ý ĐỊNH (AI) ---
    print("\n--- BƯỚC 2: SUY LUẬN (GEMINI AI) ---")
    keyword = filter_mod.get_smart_keyword(raw_text)
    print(f"🧠 AI đoán bạn muốn tìm: '{keyword}'")

    # --- BƯỚC 3: TÌM KIẾM (SEARCH) ---
    print("\n--- BƯỚC 3: TÌM KIẾM  ---")
    
    links = search_mod.google_search(keyword)
    
    print(f"\n✅ KẾT QUẢ CUỐI CÙNG ({len(links)} link):")
    if links:
        for i, link in enumerate(links, 1):
            print(f"{i}. {link}")
    else:
        print("   (Không tìm thấy link nào)")

if __name__ == "__main__":
    chay_demo()