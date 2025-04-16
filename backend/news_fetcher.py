import feedparser
import json
import os
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import re
import time
from config import config
from embeddings import EmbeddingGenerator
from vector_store import VectorStore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('news_fetcher.log')
    ]
)
logger = logging.getLogger('NewsFetcher')

class NewsFetcher:
    def __init__(
        self,
        embedding_generator: Optional[EmbeddingGenerator] = None,
        vector_store: Optional[VectorStore] = None,
        max_retries: int = 3,
        retry_delay: int = 5
    ):
        self.feeds = config.rss_feeds
        self.embedding_generator = embedding_generator or EmbeddingGenerator()
        self.vector_store = vector_store or VectorStore()
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        logger.info("NewsFetcher initialized with %d RSS feeds", len(self.feeds))

    def clean_html_content(self, html_content: str) -> str:
        """Clean HTML content and extract plain text."""
        logger.debug("Cleaning HTML content of length %d", len(html_content))
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        cleaned_text = text.strip()
        logger.debug("Cleaned text length: %d", len(cleaned_text))
        return cleaned_text

    def fetch_rss_news(self, feed_url: str) -> List[Dict[str, Any]]:
        """Fetch news articles from a single RSS feed with retry logic."""
        logger.info("Fetching news from feed: %s", feed_url)
        articles = []
        
        for attempt in range(self.max_retries):
            try:
                feed = feedparser.parse(feed_url)
                if not feed.entries:
                    logger.warning("No entries found in feed %s (attempt %d/%d)", 
                                 feed_url, attempt + 1, self.max_retries)
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                        continue
                    return []
                
                for entry in feed.entries:
                    # Get raw content with HTML
                    raw_content = entry.get("summary", "")
                    
                    # Clean HTML content
                    clean_content = self.clean_html_content(raw_content)
                    
                    article = {
                        "title": entry.title,
                        "raw_content": raw_content,  # Store original HTML content
                        "content": clean_content,     # Store cleaned text content
                        "link": entry.get("link", ""),
                        "published": entry.get("published", datetime.now().isoformat()),
                        "source": feed.feed.get("title", "Unknown"),
                        "categories": [tag.term for tag in entry.get("tags", [])],
                        "id": entry.get("id", entry.get("link", "")),
                    }
                    articles.append(article)
                
                logger.info("Fetched %d articles from %s", len(articles), feed_url)
                return articles
                
            except Exception as e:
                logger.error("Error fetching from %s (attempt %d/%d): %s", 
                           feed_url, attempt + 1, self.max_retries, str(e))
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    logger.error("Failed to fetch from %s after %d attempts", 
                               feed_url, self.max_retries)
                    return []

    def fetch_all_news(self) -> List[Dict[str, Any]]:
        """Fetch news from all configured RSS feeds."""
        logger.info("Starting to fetch news from all %d feeds", len(self.feeds))
        all_articles = []
        
        for feed_url in self.feeds:
            articles = self.fetch_rss_news(feed_url)
            all_articles.extend(articles)
            logger.info("Successfully fetched %d articles from %s", len(articles), feed_url)
        
        logger.info("Total articles fetched: %d", len(all_articles))
        return all_articles

    def save_raw_articles(self, articles: List[Dict[str, Any]]) -> str:
        """Save raw articles to a JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"raw_news_{timestamp}.json"
        filepath = os.path.join(config.raw_news_dir, filename)
        
        logger.info("Saving %d raw articles to %s", len(articles), filepath)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        
        logger.info("Raw articles saved successfully")
        return filepath

    def save_processed_articles(self, articles: List[Dict[str, Any]]) -> str:
        """Save processed articles with embeddings to a JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"processed_news_{timestamp}.json"
        filepath = os.path.join(config.processed_news_dir, filename)
        
        # Create a copy of articles without raw_content for processed storage
        processed_articles = []
        for article in articles:
            processed_article = article.copy()
            processed_article.pop('raw_content', None)  # Remove raw_content from processed articles
            processed_articles.append(processed_article)
        
        logger.info("Saving %d processed articles to %s", len(processed_articles), filepath)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(processed_articles, f, ensure_ascii=False, indent=2)
        
        logger.info("Processed articles saved successfully")
        return filepath

    def process(self) -> Dict[str, Any]:
        """Main process to fetch, process, and store news articles."""
        logger.info("Starting news processing pipeline")
        
        # Fetch articles
        logger.info("Step 1: Fetching articles from RSS feeds")
        articles = self.fetch_all_news()
        if not articles:
            logger.warning("No articles found during fetching")
            return {"status": "error", "message": "No articles found"}

        # Save raw articles
        logger.info("Step 2: Saving raw articles")
        raw_filepath = self.save_raw_articles(articles)

        # Generate embeddings
        logger.info("Step 3: Generating embeddings for %d articles", len(articles))
        articles_with_embeddings = self.embedding_generator.process_articles(articles)
        logger.info("Embeddings generated successfully")

        # Save processed articles
        logger.info("Step 4: Saving processed articles with embeddings")
        processed_filepath = self.save_processed_articles(articles_with_embeddings)

        # Store in vector database
        logger.info("Step 5: Storing articles in vector database")
        success = self.vector_store.upsert_articles(articles_with_embeddings)
        
        if success:
            logger.info("Articles successfully stored in vector database")
        else:
            logger.error("Failed to store articles in vector database")

        result = {
            "status": "success" if success else "error",
            "message": "Articles processed and stored successfully" if success else "Failed to store articles",
            "raw_filepath": raw_filepath,
            "processed_filepath": processed_filepath,
            "article_count": len(articles)
        }
        
        logger.info("News processing pipeline completed with status: %s", result["status"])
        return result

