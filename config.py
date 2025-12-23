"""
Configuration file for the OCR-Search system
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

# Folder paths
INPUT_FOLDER = BASE_DIR / "image_input"
OUTPUT_FOLDER = BASE_DIR / "output"
LOG_FOLDER = BASE_DIR / "logs"

# Tesseract configuration
TESSERACT_PATH = os.getenv('TESSERACT_PATH', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
OCR_LANGUAGES = 'vie+eng'

# API Configuration - Now reads from . env file! 
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("⚠️  WARNING:  GEMINI_API_KEY not found!")
    print("Please set it in . env file or as environment variable")

GEMINI_MODEL = 'gemini-2.0-flash-exp'
GEMINI_API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent'

# Search configuration
SEARCH_REGION = 'wt-wt'
SEARCH_MAX_RESULTS = 20
SEARCH_RETURN_COUNT = 5
SEARCH_MAX_RETRIES = 3
SEARCH_RETRY_DELAY = 2

# Supported image formats
SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '. bmp', '.tiff', '.webp')

# AI Prompt template
AI_PROMPT_TEMPLATE = """
Bạn là chuyên gia lọc từ khóa tìm kiếm từ văn bản đã OCR. 
Nhiệm vụ: Từ văn bản dưới đây, trích xuất những từ khoá/từ/cụm từ có ý nghĩa thực sự (tên đề, sự kiện, đối tượng, năm, v.v...). 

YÊU CẦU:
- Chỉ giữ các cụm từ hoàn chỉnh, thông tin trọng tâm, tên, thuật ngữ, số, nơi chốn thực tế.
- **LOẠI BỎ toàn bộ dòng/ký tự lạ, ký hiệu đặc biệt, từ vô nghĩa, tiếng ồn máy OCR (ví dụ: ký tự đơn lẻ như “Q”, “£ G”, “© àb =”, “aA”, “N:”, v.v...).**
- Không dùng lại các dòng/chi tiết mà không tạo giá trị tìm kiếm trên web.
- Không lặp lại nhiều lần cùng một ý.
- Kết quả: Một danh sách từ khóa/từ/cụm từ, ngắn gọn dưới 18 từ, **không giải thích**, ngăn cách bằng dấu phẩy (,). 

Đầu vào:
{text}

Từ khóa:
""".strip()