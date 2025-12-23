"""
AI Filter Module - Phiên bản MỞ KHÓA (Tắt Safety Filter & Tăng Max Tokens)
"""
import requests
import re
import time
import json
from logger import setup_logger
from config import GEMINI_API_KEY, AI_PROMPT_TEMPLATE

logger = setup_logger('Filter')

class AIKeywordExtractor:
    def __init__(self, api_key: str = GEMINI_API_KEY):
        self.api_key = api_key
        self.model_name = "gemini-2.5-flash" 
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={api_key}"
        
        if not api_key:
            logger.warning("⚠️ Chưa cấu hình GEMINI_API_KEY!")

    def fallback_extract(self, text: str) -> str:
        """Phương án dự phòng"""
        logger.info("Using fallback (No AI)")
        text = re.sub(r'[^\w\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\-]', ' ', text)
        text = ' '.join(text.split())
        return text[:100].strip()

    def extract_keyword(self, raw_text: str, timeout: int = 60) -> str:
        if not raw_text.strip(): return ""
        if not self.api_key: return self.fallback_extract(raw_text)

        max_retries = 3
        prompt = AI_PROMPT_TEMPLATE.format(text=raw_text[:2500]) # Gửi nhiều text hơn chút
        
        headers = {'Content-Type': 'application/json'}
        
        # === CẤU HÌNH QUAN TRỌNG ĐỂ KHÔNG BỊ CẮT NGANG ===
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 500,  # Tăng lên 500 (trước là 100-200) để nó nói thoải mái
            },
            # TẮT BỘ LỌC AN TOÀN (Quan trọng nhất)
            # Giúp AI không bị hoang tưởng khi thấy ký tự lạ từ OCR
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        }

        for attempt in range(max_retries):
            try:
                response = requests.post(self.api_url, headers=headers, json=data, timeout=timeout)

                if response.status_code == 200:
                    result = response.json()
                    
                    # === DEBUG: Kiểm tra xem tại sao nó dừng ===
                    try:
                        candidate = result['candidates'][0]
                        finish_reason = candidate.get('finishReason', 'UNKNOWN')
                        
                        # Nếu lý do dừng là SAFETY (An toàn) hoặc OTHER -> Cảnh báo
                        if finish_reason != 'STOP':
                            logger.warning(f"⚠️ AI dừng bất thường. Lý do: {finish_reason}")
                        
                        content_parts = candidate.get('content', {}).get('parts', [])
                        if content_parts:
                            keyword = content_parts[0]['text'].strip()
                            # Làm sạch keyword
                            keyword = keyword.replace('"', '').replace("'", "").replace("Search Query:", "").strip().split('\n')[0]
                            
                            if len(keyword) < 3: # Nếu AI trả về quá ngắn (kiểu 1-2 chữ)
                                logger.warning("⚠️ AI trả về quá ngắn, thử lại...")
                                continue

                            logger.info(f"✅ Gemini suggested: '{keyword}'")
                            return keyword
                        else:
                            # Trường hợp bị lọc sạch bách
                            logger.warning(f"⚠️ AI trả về rỗng (Bị lọc). Lý do: {finish_reason}")
                            continue

                    except (KeyError, IndexError) as e:
                        logger.error(f"❌ Lỗi đọc JSON (Lần {attempt+1}): {e}")
                        # In thử JSON ra xem nó trả về cái quái gì
                           # print(json.dumps(result, indent=2)) 
                        time.sleep(2)
                        continue

                elif response.status_code == 429:
                    logger.warning(f"⚠️ Hết lượt (429). Nghỉ 5s...")
                    time.sleep(5)
                    continue
                else:
                    logger.error(f"❌ API Error {response.status_code}")
                    return self.fallback_extract(raw_text)

            except Exception as e:
                logger.error(f"❌ Lỗi mạng: {e}")
                time.sleep(2)

        return self.fallback_extract(raw_text)

def get_smart_keyword(raw_text: str) -> str:
    extractor = AIKeywordExtractor()
    return extractor.extract_keyword(raw_text)