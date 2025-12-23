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
AI_PROMPT_TEMPLATE = """Bạn là công cụ tối ưu hóa từ khóa tìm kiếm. 

Nhiệm vụ:  Trích xuất từ khóa tìm kiếm tốt nhất từ văn bản sau.  

Yêu cầu: 
- Từ khóa phải ngắn gọn (dưới 20 từ)
- Giữ lại TẤT CẢ thông tin quan trọng (tên, từ viết tắt, số liệu)
- Loại bỏ noise và thông tin không liên quan
- Chỉ trả về từ khóa, KHÔNG giải thích

Văn bản:  {text}

Từ khóa: """