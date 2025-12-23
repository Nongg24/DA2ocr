"""
AI Filter Module - Use Gemini to extract smart keywords with fallback
"""
import requests
import re
from typing import Optional
from logger import setup_logger
from config import GEMINI_API_KEY, GEMINI_API_URL, AI_PROMPT_TEMPLATE

logger = setup_logger('Filter')


class AIKeywordExtractor:
    """AI-powered keyword extractor using Gemini with fallback"""
    
    def __init__(self, api_key: str = GEMINI_API_KEY):
        self.api_key = api_key
        self.api_url = f"{GEMINI_API_URL}?key={api_key}"
        self.quota_exceeded = False
        
        if not api_key or api_key == 'YOUR_API_KEY_HERE':
            logger.warning("⚠️ No valid API key configured!")
        else:
            logger.info("AI Keyword Extractor initialized")
    
    def fallback_extract(self, text: str) -> str:
        """
        Simple fallback keyword extraction without AI
        """
        logger.info("Using fallback keyword extraction (no AI)")
        
        # Remove special characters but keep Vietnamese
        text = re.sub(r'[^\w\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\-]', ' ', text)
        text = ' '.join(text.split())
        
        # Take first meaningful part (max 100 chars)
        keyword = text[:100].strip()
        
        display_keyword = keyword[:50] + "..." if len(keyword) > 50 else keyword
        logger.info(f"📝 Fallback keyword:  '{display_keyword}'")
        return keyword
    
    def extract_keyword(self, raw_text: str, timeout: int = 15) -> str:
        """
        Extract keyword from text using AI with fallback
        """
        if not raw_text.strip():
            logger.warning("Empty text provided")
            return ""
        
        # If quota already exceeded, use fallback immediately
        if self.quota_exceeded:
            return self.fallback_extract(raw_text)
        
        if not self.api_key or self.api_key == 'YOUR_API_KEY_HERE': 
            logger.warning("No valid API key, using fallback")
            return self.fallback_extract(raw_text)
        
        logger.info("Sending request to Gemini API...")
        
        # Prepare prompt
        prompt = AI_PROMPT_TEMPLATE.format(text=raw_text[: 1000])
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 100,
            }
        }
        
        try:
            response = requests. post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                keyword = result['candidates'][0]['content']['parts'][0]['text']. strip()
                keyword = keyword.replace('"', '').replace("'", "")
                logger.info(f"✅ AI suggested:  '{keyword}'")
                return keyword
            
            elif response.status_code == 429:
                # Quota exceeded
                logger.warning("⚠️ API quota exceeded, switching to fallback mode")
                self.quota_exceeded = True
                return self.fallback_extract(raw_text)
            
            else:
                logger.error(f"❌ API Error ({response.status_code})")
                return self.fallback_extract(raw_text)
                
        except requests. Timeout:
            logger.error("❌ Request timeout, using fallback")
            return self. fallback_extract(raw_text)
            
        except Exception as e:
            logger.error(f"❌ Request failed: {e}, using fallback")
            return self.fallback_extract(raw_text)


def get_smart_keyword(raw_text: str) -> str:
    """Legacy function for backward compatibility"""
    extractor = AIKeywordExtractor()
    return extractor.extract_keyword(raw_text)


if __name__ == "__main__": 
    # Test
    extractor = AIKeywordExtractor()
    
    test_text = "Bộ môn Giải tích - VI TÍCH PHÂN 1 - DHQG-HCM"
    keyword = extractor.extract_keyword(test_text)
    
    print(f"\nOriginal:  {test_text}")
    print(f"Keyword: {keyword}")