"""
OCR Module - Extract text from images using Tesseract (PIL only)
"""
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from pathlib import Path
from typing import Optional
from logger import setup_logger
from config import TESSERACT_PATH, OCR_LANGUAGES

logger = setup_logger('OCR')
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


class OCRProcessor:
    """OCR Processor with PIL preprocessing"""
    
    def __init__(self, languages: str = OCR_LANGUAGES):
        self.languages = languages
        logger.info(f"OCR Processor initialized with languages: {languages}")
    
    def preprocess_image(self, image:  Image.Image) -> Image.Image:
        """Enhanced preprocessing with PIL"""
        try:
            # Convert to RGB if needed
            if image.mode not in ('L', 'RGB'):
                image = image.convert('RGB')
            
            # Convert to grayscale
            image = image. convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance. Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.5)
            
            # Apply threshold (convert to pure black/white)
            threshold = 128
            image = image. point(lambda p: 255 if p > threshold else 0)
            
            # Denoise
            image = image.filter(ImageFilter.MedianFilter(size=3))
            
            return image
        except Exception as e:
            logger.warning(f"Preprocessing failed: {e}")
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
        
        logger.info(f"Processing:   {image_path. name}")
        
        results = []
        
        try:
            image = Image.open(image_path)
            
            # Try with preprocessing
            if preprocess: 
                processed_img = self.preprocess_image(image. copy())
                text = pytesseract.image_to_string(processed_img, lang=self.languages)
                results.append(("Preprocessed", text. strip()))
                logger.debug(f"Preprocessed:  {len(text. strip())} chars")
            
            # Try raw image
            text = pytesseract.image_to_string(image, lang=self.languages)
            results. append(("Raw", text.strip()))
            logger.debug(f"Raw: {len(text. strip())} chars")
            
        except Exception as e:
            logger.error(f"OCR failed: {e}", exc_info=True)
            return None
        
        # Return the longest result
        if results:
            best_method, best_text = max(results, key=lambda x: len(x[1]))
            
            if best_text:
                logger.info(f"✅ Extracted {len(best_text)} characters (method: {best_method})")
                logger.debug(f"Preview: {best_text[:100]}...")
                return best_text
            else:
                logger. warning("⚠️ No text extracted")
                return None
        
        return None


def extract_text_from_image(image_path: str) -> str:
    """Legacy function for backward compatibility"""
    processor = OCRProcessor()
    result = processor.extract_text(image_path)
    return result if result else ""


if __name__ == "__main__":
    # Test
    processor = OCRProcessor()
    test_image = "image_input/test.jpg"
    
    if Path(test_image).exists():
        text = processor.extract_text(test_image)
        print(f"\nExtracted text:\n{text}")
    else:
        print(f"Test image not found: {test_image}")