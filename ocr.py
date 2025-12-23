"""
OCR Module - Extract text from images using Tesseract
"""
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from pathlib import Path
from typing import Optional
from logger import setup_logger
from config import TESSERACT_PATH, OCR_LANGUAGES

logger = setup_logger('OCR')

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


class OCRProcessor:
    """OCR Processor with image preprocessing capabilities"""
    
    def __init__(self, languages: str = OCR_LANGUAGES):
        self.languages = languages
        logger.info(f"OCR Processor initialized with languages: {languages}")
    
    def preprocess_image(self, image:  Image.Image) -> Image.Image:
        """Preprocess image for better OCR results"""
        try:
            # Convert to grayscale
            image = image.convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance. Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Sharpen
            image = image.filter(ImageFilter. SHARPEN)
            
            return image
        except Exception as e:
            logger.warning(f"Preprocessing failed: {e}. Using original image.")
            return image
    
    def extract_text(self, image_path: str, preprocess: bool = True) -> Optional[str]:
        """
        Extract text from image
        
        Args:
            image_path: Path to image file
            preprocess: Whether to preprocess image
            
        Returns: 
            Extracted text or None if failed
        """
        image_path = Path(image_path)
        
        if not image_path.exists():
            logger.error(f"Image not found: {image_path}")
            return None
        
        logger.info(f"Processing:  {image_path. name}")
        
        try: 
            # Open image
            image = Image.open(image_path)
            logger.debug(f"Image size: {image.size}, mode: {image.mode}")
            
            # Preprocess if needed
            if preprocess:
                image = self.preprocess_image(image)
            
            # Extract text
            text = pytesseract.image_to_string(image, lang=self.languages)
            text = text.strip()
            
            if text:
                logger.info(f"✅ Extracted {len(text)} characters")
                logger.debug(f"Preview: {text[:100]}...")
            else:
                logger.warning("⚠️ No text extracted")
            
            return text
            
        except Exception as e:
            logger.error(f"❌ OCR failed: {e}", exc_info=True)
            return None


def extract_text_from_image(image_path: str) -> str:
    """Legacy function for backward compatibility"""
    processor = OCRProcessor()
    result = processor.extract_text(image_path)
    return result if result else ""


if __name__ == "__main__": 
    # Test
    processor = OCRProcessor()
    test_image = "image_input/test. jpg"
    
    if Path(test_image).exists():
        text = processor.extract_text(test_image)
        print(f"\nExtracted text:\n{text}")
    else:
        print(f"Test image not found: {test_image}")