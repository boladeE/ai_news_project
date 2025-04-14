from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import json
import os

from news_fetcher import NewsFetcher
from embeddings import EmbeddingGenerator
from vector_store import VectorStore
from recommender import NewsRecommender
from config import RAW_NEWS_DIR, PROCESSED_NEWS_DIR

app = FastAPI(title="DS Task AI News API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
news_fetcher = NewsFetcher()
embedding_generator = EmbeddingGenerator()
vector_store = VectorStore()
recommender = NewsRecommender()

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "DS Task AI News API",
        "version": "1.0.0",
        "description": "AI-powered news retrieval and recommendation system"
    }

@app.get("/fetch-news")
async def fetch_news():
    """Fetch news from RSS feeds and store in vector database."""
    try:
        result = news_fetcher.process()
        if result["status"] == "error":
            raise HTTPException(status_code=404, detail=result["message"])
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recommend-news")
async def recommend_news(article_id: str = None, query: str = None):
    """Get news recommendations based on article ID or search query."""
    try:
        if article_id:
            # Get article from vector store
            article = vector_store.search_similar([0] * 4096, top_k=1)  # Placeholder vector
            if not article:
                raise HTTPException(status_code=404, detail="Article not found")
            
            # Generate query embedding from article content
            query_embedding = embedding_generator.get_query_embedding(
                f"{article[0]['title']} {article[0]['content']}"
            )
        elif query:
            # Generate query embedding from search query
            query_embedding = embedding_generator.get_query_embedding(query)
        else:
            raise HTTPException(
                status_code=400,
                detail="Either article_id or query parameter is required"
            )

        # Search for similar articles
        similar_articles = vector_store.search_similar(query_embedding)
        if not similar_articles:
            raise HTTPException(status_code=404, detail="No similar articles found")

        # Generate insights for the articles
        insights = recommender.analyze_articles(similar_articles)

        return {
            "articles": similar_articles,
            "insights": insights
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/article/{article_id}")
async def get_article(article_id: str):
    """Get a specific article and its summary."""
    try:
        # Search for the article
        articles = vector_store.search_similar([0] * 4096, top_k=1)  # Placeholder vector
        if not articles:
            raise HTTPException(status_code=404, detail="Article not found")

        article = articles[0]
        
        # Generate summary
        summary = recommender.generate_summary(article)

        return {
            "article": article,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
