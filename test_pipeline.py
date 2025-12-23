"""
Comprehensive testing script for the OCR-Search pipeline
"""
import sys
from pathlib import Path
from logger import setup_logger
from ocr import OCRProcessor
from filter import AIKeywordExtractor
from search import WebSearcher

logger = setup_logger('Test')


def test_ocr():
    """Test OCR functionality"""
    logger.info("\n" + "="*60)
    logger.info("Testing OCR Module")
    logger.info("="*60)
    
    processor = OCRProcessor()
    test_image = Path("image_input/test.jpg")
    
    if not test_image.exists():
        logger.warning(f"Test image not found: {test_image}")
        return False
    
    text = processor.extract_text(test_image)
    
    if text:
        logger.info(f"✅ OCR Test PASSED")
        logger.info(f"Extracted text preview:\n{text[:200]}...")
        return True
    else:
        logger.error("❌ OCR Test FAILED")
        return False


def test_ai_filter():
    """Test AI filter functionality"""
    logger.info("\n" + "="*60)
    logger.info("Testing AI Filter Module")
    logger.info("="*60)
    
    extractor = AIKeywordExtractor()
    
    test_texts = [
        "Bộ môn Giải tích - VI TÍCH PHÂN 1 - DHQG-HCM",
        "Python Programming:  From Basics to Advanced",
        "機械学習とディープラーニングの基礎"
    ]
    
    results = []
    for text in test_texts:
        keyword = extractor.extract_keyword(text)
        results.append(bool(keyword))
        logger.info(f"Input: {text}")
        logger.info(f"Output: {keyword}\n")
    
    if all(results):
        logger.info("✅ AI Filter Test PASSED")
        return True
    else:
        logger.error("❌ AI Filter Test FAILED")
        return False


def test_search():
    """Test search functionality"""
    logger.info("\n" + "="*60)
    logger.info("Testing Search Module")
    logger.info("="*60)
    
    searcher = WebSearcher()
    
    test_queries = [
        "vi tích phân giáo trình",
        "python tutorial",
        "machine learning basics"
    ]
    
    results = []
    for query in test_queries:
        urls = searcher.search(query)
        results.append(len(urls) > 0)
        logger.info(f"Query: {query}")
        logger.info(f"Found:  {len(urls)} URLs\n")
    
    if any(results):
        logger.info("✅ Search Test PASSED")
        return True
    else:
        logger.error("❌ Search Test FAILED")
        return False


def main():
    """Run all tests"""
    logger.info("\n" + "#"*60)
    logger.info("# STARTING COMPREHENSIVE PIPELINE TESTS")
    logger.info("#"*60)
    
    tests = [
        ("OCR", test_ocr),
        ("AI Filter", test_ai_filter),
        ("Search", test_search)
    ]
    
    results = {}
    
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            logger.error(f"❌ {name} test crashed: {e}", exc_info=True)
            results[name] = False
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("TEST SUMMARY")
    logger.info("="*60)
    
    for name, passed in results. items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        logger.info(f"{name}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    logger.info("="*60)
    logger.info(f"Total:  {passed}/{total} tests passed")
    logger.info("="*60)
    
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())