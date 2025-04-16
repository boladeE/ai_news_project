import cohere
from typing import List, Dict, Any, Optional
from config import config

class EmbeddingGenerator:
    def __init__(self, cohere_client: Optional[cohere.Client] = None):
        self.client = cohere_client or cohere.Client(config.cohere_api_key)

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts using Cohere."""
        try:
            response = self.client.embed(
                texts=texts,
                model="embed-english-v3.0",
                input_type="search_document"
            )
            return response.embeddings
        except Exception as e:
            print(f"Error generating embeddings: {str(e)}")
            return []

    def process_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process articles and add embeddings to them."""
        # Prepare texts for embedding
        texts = [
            f"{article['title']} {article['content']}" 
            for article in articles
        ]
        
        # Generate embeddings
        embeddings = self.generate_embeddings(texts)
        
        # Add embeddings to articles
        for article, embedding in zip(articles, embeddings):
            article["embedding"] = embedding
        
        return articles

    def get_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for a search query."""
        try:
            response = self.client.embed(
                texts=[query],
                model="embed-english-v3.0",
                input_type="search_query"
            )
            return response.embeddings[0]
        except Exception as e:
            print(f"Error generating query embedding: {str(e)}")
            return []
