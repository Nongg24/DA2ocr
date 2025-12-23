"""
AI Filter Module - Use Gemini to extract smart keywords
"""
import requests
from typing import Optional
from logger import setup_logger
from config import GEMINI_API_KEY, GEMINI_API_URL, AI_PROMPT_TEMPLATE

logger = setup_logger('Filter')


class AIKeywordExtractor:
    """AI-powered keyword extractor using Gemini"""
    
    def __init__(self, api_key: str = GEMINI_API_KEY):
        self.api_key = api_key
        self.api_url = f"{GEMINI_API_URL}?key={api_key}"
        
        if not api_key or api_key == 'YOUR_API_KEY_HERE':
            logger.warning("⚠️ No valid API key configured!")
        else:
            logger.info("AI Keyword Extractor initialized")
    
    def extract_keyword(self, raw_text: str, timeout: int = 15) -> str:
        """
        Extract keyword from text using AI
        
        Args:
            raw_text: Raw text to process
            timeout: Request timeout in seconds
            
        Returns:
            Extracted keyword (or original text if failed)
        """
        if not raw_text. strip():
            logger.warning("Empty text provided")
            return ""
        
        if not self.api_key or self.api_key == 'YOUR_API_KEY_HERE': 
            logger.error("No valid API key.  Returning original text.")
            return raw_text
        
        logger.info("Sending request to Gemini API...")
        
        # Prepare prompt
        prompt = AI_PROMPT_TEMPLATE.format(text=raw_text[: 1000])  # Limit text length
        
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
                
                # Extract keyword from response
                keyword = result['candidates'][0]['content']['parts'][0]['text']. strip()
                keyword = keyword.replace('"', '').replace("'", "")
                
                logger.info(f"✅ AI suggested:  '{keyword}'")
                return keyword
                
            else:
                logger.error(f"❌ API Error ({response.status_code}): {response.text}")
                return raw_text
                
        except requests. Timeout:
            logger.error("❌ Request timeout")
            return raw_text
            
        except Exception as e:
            logger.error(f"❌ Request failed: {e}", exc_info=True)
            return raw_text


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