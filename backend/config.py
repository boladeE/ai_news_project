import os
from dotenv import load_dotenv

# Load environment variables

# Construct the path to the .env file
# dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')

# Load environment variables from the specified path
load_dotenv()

# API Keys
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Pinecone Configuration
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "news-articles")

# News Sources
RSS_FEEDS = [
    # "https://feeds.feedburner.com/TechCrunch/",
    # "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/rss",
    "https://www.technologyreview.com/feed/",
]

# Vector Database Settings
VECTOR_DIMENSION = 1024  # Cohere embedding dimension
TOP_K_RESULTS = 5

# Data Directories
RAW_NEWS_DIR = "data/raw_news"
PROCESSED_NEWS_DIR = "data/processed_news"

# Create directories if they don't exist
os.makedirs(RAW_NEWS_DIR, exist_ok=True)
os.makedirs(PROCESSED_NEWS_DIR, exist_ok=True)
