"""
Main Module - Orchestrate OCR -> Filter -> Search pipeline
"""
import sys
from pathlib import Path
from typing import List, Tuple
from datetime import datetime
import time

from logger import setup_logger
from config import (
    INPUT_FOLDER,
    OUTPUT_FOLDER,
    SUPPORTED_FORMATS
)

# Import processors
from ocr import OCRProcessor
from filter import AIKeywordExtractor
from search import WebSearcher

logger = setup_logger('Main')


class ImageProcessor:
    """Main processor orchestrating the pipeline"""
    
    def __init__(self):
        self.ocr = OCRProcessor()
        self.ai_filter = AIKeywordExtractor()
        self.searcher = WebSearcher()
        
        # Ensure folders exist
        INPUT_FOLDER.mkdir(exist_ok=True)
        OUTPUT_FOLDER.mkdir(exist_ok=True)
        
        logger.info("="*60)
        logger.info("Image Processor initialized")
        logger.info(f"Input folder: {INPUT_FOLDER}")
        logger.info(f"Output folder: {OUTPUT_FOLDER}")
        logger.info("="*60)
    
    def save_results(
        self,
        filename: str,
        raw_text: str,
        keyword: str,
        urls: List[str]
    ) -> bool:
        """
        Save processing results to file with proper UTF-8 encoding
        
        Args:  
            filename: Original image filename
            raw_text: OCR extracted text
            keyword: AI filtered keyword
            urls: Search results URLs
            
        Returns:  
            True if successful, False otherwise
        """
        output_file = OUTPUT_FOLDER / f"{filename}.txt"
        
        try:
            # Use UTF-8 with BOM for proper Vietnamese display in Windows
            with open(output_file, "w", encoding="utf-8-sig") as f:
                f.write("="*70 + "\n")
                f.write(f" KẾT QUẢ XỬ LÝ: {filename}\n")
                f.write(f" Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*70 + "\n\n")
                
                f.write("[1] VĂN BẢN GỐC (OCR)\n")
                f.write("-"*70 + "\n")
                f.write(f"{raw_text}\n\n")
                
                f.write("[2] TỪ KHÓA TÌM KIẾM (AI)\n")
                f.write("-"*70 + "\n")
                f.write(f"{keyword}\n\n")
                
                f. write("[3] KẾT QUẢ TÌM KIẾM\n")
                f.write("-"*70 + "\n")
                
                if urls: 
                    for i, url in enumerate(urls, 1):
                        f.write(f"{i}. {url}\n")
                else:
                    f.write("Không tìm thấy kết quả nào.\n")
                
                f.write("\n" + "="*70 + "\n")
                f.write("Xử lý hoàn tất!\n")
            
            logger.info(f"💾 Saved: {output_file. name}")
            return True
            
        except Exception as e:  
            logger.error(f"❌ Failed to save results: {e}", exc_info=True)
            return False
    
    def process_image(self, image_path: Path) -> Tuple[bool, str]:
        """
        Process single image through complete pipeline
        
        Args:  
            image_path: Path to image file
            
        Returns: 
            Tuple of (success, message)
        """
        filename = image_path.name
        logger.info(f"\n{'='*60}")
        logger.info(f"🖼️  Processing: {filename}")
        logger.info(f"{'='*60}")
        
        try:
            # Step 1: OCR
            raw_text = self.ocr. extract_text(image_path)
            if not raw_text:  
                msg = "⚠️ No text extracted, skipping"
                logger.warning(msg)
                return False, msg
            
            # Step 2: AI Filter
            keyword = self.ai_filter.extract_keyword(raw_text)
            if not keyword: 
                keyword = raw_text  # Fallback
            
            # Step 3: Search
            urls = self.searcher.search(keyword)
            
            # Step 4: Save results
            success = self.save_results(filename, raw_text, keyword, urls)
            
            if success:  
                return True, "✅ Success"
            else:
                return False, "❌ Failed to save"
                
        except Exception as e:
            msg = f"❌ Error:  {e}"
            logger.error(msg, exc_info=True)
            return False, msg
    
    def process_all(self, delay: float = 1.5) -> Tuple[int, int]:
        """
        Process all images in input folder
        
        Args:  
            delay: Delay between processing images (seconds)
            
        Returns:  
            Tuple of (successful_count, total_count)
        """
        # Find all image files
        image_files = [
            f for f in INPUT_FOLDER.iterdir()
            if f.is_file() and f.suffix.lower() in SUPPORTED_FORMATS
        ]
        
        if not image_files:
            logger.warning(f"⚠️ No images found in {INPUT_FOLDER}")
            logger.info(f"Supported formats: {', '.join(SUPPORTED_FORMATS)}")
            return 0, 0
        
        logger.info(f"\n🎯 Found {len(image_files)} image(s) to process")
        logger.info(f"📁 Results will be saved to: {OUTPUT_FOLDER}")
        
        successful = 0
        
        for i, image_path in enumerate(image_files, 1):
            logger.info(f"\n[{i}/{len(image_files)}]")
            
            success, message = self.process_image(image_path)
            if success:
                successful += 1
            
            # Delay between images (except last one)
            if i < len(image_files):
                logger.debug(f"Waiting {delay}s before next image...")
                time.sleep(delay)
        
        return successful, len(image_files)


def main():
    """Main entry point"""
    try:
        processor = ImageProcessor()
        
        start_time = time.time()
        successful, total = processor.process_all()
        elapsed = time.time() - start_time
        
        # Summary
        logger.info("\n" + "="*60)
        logger.info("📊 PROCESSING SUMMARY")
        logger.info("="*60)
        logger.info(f"✅ Successful: {successful}/{total}")
        logger.info(f"❌ Failed: {total - successful}/{total}")
        logger.info(f"⏱️  Time elapsed: {elapsed:.2f}s")
        logger.info(f"📁 Results saved to: {OUTPUT_FOLDER}")
        logger.info("="*60)
        
        if successful > 0:
            logger.info("\n🎉 Processing complete!")
        else:
            logger.warning("\n⚠️ No images were successfully processed")
        
        return 0 if successful == total else 1
        
    except KeyboardInterrupt:
        logger. warning("\n⚠️ Process interrupted by user")
        return 130
        
    except Exception as e:  
        logger.error(f"\n❌ Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())