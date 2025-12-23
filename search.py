"""
Search Module - Find relevant URLs using DuckDuckGo
"""
import time
import random
from typing import List
from duckduckgo_search import DDGS
from logger import setup_logger
from config import (
    SEARCH_REGION,
    SEARCH_MAX_RESULTS,
    SEARCH_RETURN_COUNT,
    SEARCH_MAX_RETRIES,
    SEARCH_RETRY_DELAY
)

logger = setup_logger('Search')


class WebSearcher:
    """Web searcher using DuckDuckGo"""
    
    def __init__(
        self,
        region: str = SEARCH_REGION,
        max_results: int = SEARCH_MAX_RESULTS,
        return_count: int = SEARCH_RETURN_COUNT,
        max_retries: int = SEARCH_MAX_RETRIES
    ):
        self.region = region
        self.max_results = max_results
        self. return_count = return_count
        self.max_retries = max_retries
        logger.info(f"Web Searcher initialized (max_results={max_results}, return={return_count})")
    
    def search(self, query: str) -> List[str]:
        """
        Search for URLs using query
        
        Args:
            query: Search query
            
        Returns:
            List of URLs (up to return_count)
        """
        if not query.strip():
            logger.warning("Empty query provided")
            return []
        
        logger.info(f"Searching for: '{query}'")
        
        urls = []
        
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.debug(f"Attempt {attempt}/{self.max_retries}")
                
                # Perform search
                results = DDGS().text(
                    query,
                    region=self.region,
                    safesearch='off',
                    max_results=self.max_results
                )
                
                if results:
                    for item in results:
                        url = item.get('href')
                        if url and url not in urls:
                            urls.append(url)
                            
                            # Stop if we have enough
                            if len(urls) >= self.return_count:
                                break
                    
                    if urls:
                        logger.info(f"✅ Found {len(urls)} URL(s)")
                        break
                else:
                    logger.warning(f"No results on attempt {attempt}")
                    
            except Exception as e:
                logger.error(f"❌ Search error (attempt {attempt}): {e}")
            
            # Wait before retry
            if attempt < self.max_retries:
                delay = SEARCH_RETRY_DELAY + random.uniform(0, 2)
                logger.debug(f"Waiting {delay:. 1f}s before retry...")
                time.sleep(delay)
        
        if not urls:
            logger.warning("⚠️ No URLs found after all attempts")
        elif len(urls) < self.return_count:
            logger.info(f"⚠️ Only found {len(urls)}/{self.return_count} URLs")
        
        return urls[: self.return_count]


def google_search(query: str) -> List[str]:
    """Legacy function for backward compatibility"""
    searcher = WebSearcher()
    return searcher.search(query)


if __name__ == "__main__":
    # Test
    searcher = WebSearcher()
    
    test_query = "python programming tutorial"
    results = searcher.search(test_query)
    
    print(f"\nSearch results for:  {test_query}")
    for i, url in enumerate(results, 1):
        print(f"{i}. {url}")