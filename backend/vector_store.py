from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Any
from config import (
    PINECONE_API_KEY,
    PINECONE_ENVIRONMENT,
    PINECONE_INDEX_NAME,
    VECTOR_DIMENSION,
    TOP_K_RESULTS
)

class VectorStore:
    def __init__(self):
        self.pinecone = Pinecone(api_key=PINECONE_API_KEY)
        self.index_name = PINECONE_INDEX_NAME
        self._ensure_index()

    def _ensure_index(self):
        """Ensure the Pinecone index exists, create if it doesn't."""
        if self.index_name not in self.pinecone.list_indexes().names():
            self.pinecone.create_index(
                name=self.index_name,
                dimension=VECTOR_DIMENSION,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
        self.index = self.pinecone.Index(self.index_name)

    def upsert_articles(self, articles: List[Dict[str, Any]]) -> bool:
        """Upsert articles to the vector store."""
        try:
            vectors = []
            for article in articles:
                if "embedding" not in article:
                    continue
                    
                vector = {
                    "id": article["id"],
                    "values": article["embedding"],
                    "metadata": {
                        "title": article["title"],
                        "content": article["content"],
                        "link": article["link"],
                        "published": article["published"],
                        "source": article["source"],
                        "categories": article["categories"]
                    }
                }
                vectors.append(vector)

            if vectors:
                self.index.upsert(vectors=vectors)
            return True
        except Exception as e:
            print(f"Error upserting articles: {str(e)}")
            return False

    def search_similar(self, query_embedding: List[float], top_k: int = TOP_K_RESULTS) -> List[Dict[str, Any]]:
        """Search for similar articles using the query embedding."""
        try:
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            articles = []
            for match in results.matches:
                article = {
                    "id": match.id,
                    "score": match.score,
                    **match.metadata
                }
                articles.append(article)
            
            return articles
        except Exception as e:
            print(f"Error searching similar articles: {str(e)}")
            return []

    def delete_article(self, article_id: str) -> bool:
        """Delete an article from the vector store."""
        try:
            self.index.delete(ids=[article_id])
            return True
        except Exception as e:
            print(f"Error deleting article: {str(e)}")
            return False

