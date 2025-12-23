# DA2OCR - Vietnamese Document OCR & AI Search Pipeline

DA2OCR là pipeline nhận diện văn bản tiếng Việt (OCR) từ ảnh, trích xuất từ khóa thông minh với AI, và gợi ý link tra cứu trực tuyến.

## 📦 Tính năng nổi bật
- Nhận diện tiếng Việt/Anh từ ảnh bằng Tesseract
- Tự động trích xuất từ khóa tìm kiếm bằng AI Gemini (Google)
- Lọc nhiễu mạnh, loại bỏ rác OCR (1 ký tự, ký hiệu lạ)
- Gợi ý top link tài liệu từ DuckDuckGo Search
- Lưu kết quả tiếng Việt chuẩn ra file `.txt` hoặc HTML
- Dễ dàng cấu hình qua file `.env`

---

## 🚀 Hướng dẫn sử dụng nhanh

### 1. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 2. Cài [Tesseract OCR](https://github.com/tesseract-ocr/tessdoc#binaries) (bản Windows hoặc Linux)
- **Windows:** Đường dẫn ví dụ: `C:/Program Files/Tesseract-OCR/tesseract.exe`
- Cần cài gói ngôn ngữ: `vie` (Vietnamese)

### 3. Thiết lập cấu hình `.env`
- **KHÔNG sửa trực tiếp `.envexample`**
- Copy từ mẫu:
  ```bash
  cp .envexample .env # Hoặc tự tạo file .env
  ```
- **Sửa các thông tin:**
  - `GEMINI_API_KEY`: Điền API Gemini thật (lấy tại [Google AI Studio](https://aistudio.google.com/app/apikey))
  - `TESSERACT_PATH`: Đúng với đường dẫn tesseract trên máy bạn
  - `OCR_LANGUAGES`: Khuyên dùng `vie+eng`
  - Điều chỉnh folder input/output nếu bạn muốn

### 4. Đặt file ảnh vào thư mục input (mặc định: `image_input/`)
- Hỗ trợ: png, jpg, jpeg

### 5. Chạy pipeline
```bash
python main.py
```

### 6. Xem kết quả
- Trong thư mục `output/`: file `.txt` cho từng ảnh
- Tạo báo cáo HTML tổng hợp:
  ```bash
  python export_html.py
  ```
- Mở file `output/summary_report.html` trong trình duyệt

---

## ⚠️ LƯU Ý QUAN TRỌNG

- **KHÔNG commit file `.env` thật (chứa API key) lên GitHub.**  
  Luôn sử dụng `.envexample` để chia sẻ nơi đặt key/cấu hình nhưng không lộ thông tin nhạy cảm.
- **GEMINI_API_KEY miễn phí có giới hạn**. Khi hết quota, pipeline sẽ tự động bật chế độ fallback lọc keyword bằng rule nội bộ (vẫn đảm bảo kết quả sạch).
- **OCR tiếng Việt cần "vie.traineddata".** Nếu lỗi tiếng Việt, kiểm tra lại tesseract data folder.
- **Nếu ảnh chất lượng thấp, OCR có thể bị lỗi.** Đảm bảo ảnh rõ nét, không nghiêng, độ tương phản tốt để kết quả tối ưu.
- **Mọi cấu hình đều chỉnh được qua `.env`.** Nếu đổi tên folder, đường dẫn Tesseract, số link search, hãy cập nhật lại file `.env`.

---

## 🛡️ Quyền riêng tư & bảo mật

- Không chia sẻ các file kết quả/tệp cấu hình chứa thông tin nhạy cảm (API key, file người dùng...) cho bên thứ ba.
- API key sử dụng chỉ cho mục đích cá nhân/phi thương mại trừ khi bạn có thoả thuận riêng với Google.

---

## 📄 Ví dụ về file cấu hình `.env`
```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
TESSERACT_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe
OCR_LANGUAGES=vie+eng
SEARCH_REGION=vn-vi
SEARCH_MAX_RESULTS=20
SEARCH_RETURN_COUNT=5
SEARCH_MAX_RETRIES=2
SEARCH_RETRY_DELAY=2
INPUT_FOLDER=./image_input
OUTPUT_FOLDER=./output
```

---

<p>vibecode project</p>
