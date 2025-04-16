from dataclasses import dataclass, field
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class Config:
    # API Keys
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "")
    api_token: str = os.getenv("API_TOKEN", "default_secret_token")  # Default token for development

    # Pinecone Configuration
    pinecone_index_name: str = os.getenv("PINECONE_INDEX_NAME", "news-articles")
    vector_dimension: int = 1024  # Cohere embedding dimension
    top_k_results: int = 5

    # News Sources
    rss_feeds: List[str] = field(default_factory=lambda: [
        # "https://feeds.feedburner.com/TechCrunch/",
        # "https://www.theverge.com/rss/index.xml",
        "https://www.wired.com/feed/rss",
        "https://www.technologyreview.com/feed/",
    ])

    # Data Directories
    raw_news_dir: str = "data/raw_news"
    processed_news_dir: str = "data/processed_news"

    def __post_init__(self):
        # Create directories if they don't exist
        os.makedirs(self.raw_news_dir, exist_ok=True)
        os.makedirs(self.processed_news_dir, exist_ok=True)

# Create a global config instance
config = Config()

