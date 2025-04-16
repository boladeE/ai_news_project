from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List, Dict, Any
import json
import os

from news_fetcher import NewsFetcher
from embeddings import EmbeddingGenerator
from vector_store import VectorStore
from recommender import NewsRecommender
from config import config
from fastapi import HTTPException

app = FastAPI(title="DS Task AI News API")

# Configure templates
templates = Jinja2Templates(directory="backend/templates")

def verify_api_token(token: str):
    if token == config.api_token:
        print(f"API key verified: {token}")
        return token
    return None

# Add custom filters
def from_json(value):
    """Parse a JSON string into a Python object."""
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return None

templates.env.filters["from_json"] = from_json

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

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root endpoint returning the home page with links to other routes."""
    return templates.TemplateResponse(
        "home.html",
        {"request": request}
    )

@app.get("/fetch-news", response_class=HTMLResponse)
def fetch_news(request: Request, token: str = Depends(verify_api_token)):
    # print(f"Fetching news with token: {token}")
    """Fetch news from RSS feeds and store in vector database."""
    try:
        result = news_fetcher.process()
        if result["status"] == "error":
            raise HTTPException(status_code=404, detail=result["message"])
        
        # Get the latest processed articles
        processed_files = sorted(os.listdir(config.processed_news_dir), reverse=True)
        if not processed_files:
            raise HTTPException(status_code=404, detail="No processed articles found")
        
        latest_file = os.path.join(config.processed_news_dir, processed_files[0])
        with open(latest_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
            
        # Ensure each article has a link
        for article in articles:
            if 'link' not in article or not article['link']:
                # If no link is available, use the article ID as a fallback
                article['link'] = f"/article/{article.get('id', '')}"
        
        return templates.TemplateResponse(
            "news.html",
            {"request": request, "articles": articles}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recommend-news", response_class=HTMLResponse)
async def recommend_news(request: Request, article_id: str = None, query: str = None, token: str = Depends(verify_api_token)):
    """Get news recommendations based on article ID or search query."""
    try:
        if article_id:
            # Get article from vector store
            article = vector_store.search_similar([0] * 1024, top_k=1)  # Placeholder vector with correct dimension
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

        # Ensure each article has a link
        for article in similar_articles:
            if 'link' not in article or not article['link']:
                # If no link is available, use the article ID as a fallback
                article['link'] = f"/article/{article.get('id', '')}"

        # Generate insights for the articles
        insights = recommender.analyze_articles(similar_articles)

        return templates.TemplateResponse(
            "recommendations.html",
            {
                "request": request,
                "articles": similar_articles,
                "insights": insights
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/article/{article_id}")
async def get_article(article_id: str, token: str = Depends(verify_api_token)):
    """Get a specific article and its summary."""
    try:
        # Search for the article
        articles = vector_store.search_similar([0] * 1024, top_k=1)  # Placeholder vector with correct dimension
        if not articles:
            raise HTTPException(status_code=404, detail="Article not found")

        article = articles[0]
        
        # Ensure the article has a link
        if 'link' not in article or not article['link']:
            # If no link is available, use the article ID as a fallback
            article['link'] = f"/article/{article.get('id', '')}"
        
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
    uvicorn.run(app, host="localhost", port=8000)
