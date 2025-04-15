# DS Task AI News - Technical Documentation

## Architecture Overview

The DS Task AI News application is built using a modular architecture with the following components:

1. **FastAPI Backend**: Handles HTTP requests and serves HTML templates.
2. **News Fetcher**: Fetches news articles from RSS feeds.
3. **Embedding Generator**: Generates embeddings for articles using Cohere.
4. **Vector Store**: Stores and retrieves article embeddings using Pinecone.
5. **News Recommender**: Generates insights and recommendations using Groq.
6. **HTML Templates**: Renders the user interface.

## Component Details

### 1. FastAPI Backend (`main.py`)

The FastAPI backend serves as the entry point for the application. It handles HTTP requests and serves HTML templates. The backend includes the following endpoints:

- `/`: Home page with links to other routes.
- `/fetch-news`: Fetches news from RSS feeds and displays the latest articles.
- `/recommend-news`: Gets news recommendations based on an article ID or search query.
- `/article/{article_id}`: Gets a specific article and its summary.

### 2. News Fetcher (`news_fetcher.py`)

The News Fetcher component is responsible for fetching news articles from RSS feeds. It performs the following tasks:

- Fetches articles from configured RSS feeds using the `feedparser` library.
- Cleans HTML content to extract plain text.
- Saves raw articles to JSON files.
- Processes articles with embeddings.
- Saves processed articles to JSON files.
- Stores articles in the vector database.

### 3. Embedding Generator (`embeddings.py`)

The Embedding Generator component is responsible for generating embeddings for articles. It performs the following tasks:

- Generates embeddings for article content using Cohere.
- Processes articles to include embeddings.
- Generates query embeddings for search queries.

### 4. Vector Store (`vector_store.py`)

The Vector Store component is responsible for storing and retrieving article embeddings. It performs the following tasks:

- Stores article embeddings in the Pinecone vector database.
- Retrieves similar articles based on query embeddings.
- Upserts articles to update the vector database.

### 5. News Recommender (`recommender.py`)

The News Recommender component is responsible for generating insights and recommendations. It performs the following tasks:

- Analyzes articles to generate insights using Groq.
- Generates summaries for individual articles using Groq.

### 6. HTML Templates

The HTML templates are responsible for rendering the user interface. The templates include:

- `base.html`: Base template with common layout elements.
- `home.html`: Home page template.
- `news.html`: Template for displaying news articles.
- `recommendations.html`: Template for displaying recommended articles and insights.

## Data Flow

1. **Fetching News**:
   - User requests the `/fetch-news` endpoint.
   - The backend calls the News Fetcher to fetch articles from RSS feeds.
   - The News Fetcher cleans the articles and saves them to JSON files.
   - The News Fetcher calls the Embedding Generator to generate embeddings for the articles.
   - The News Fetcher calls the Vector Store to store the articles in the vector database.
   - The backend renders the `news.html` template with the fetched articles.

2. **Recommending News**:
   - User requests the `/recommend-news` endpoint with a query parameter.
   - The backend calls the Embedding Generator to generate a query embedding.
   - The backend calls the Vector Store to retrieve similar articles.
   - The backend calls the News Recommender to generate insights for the articles.
   - The backend renders the `recommendations.html` template with the recommended articles and insights.

3. **Getting an Article**:
   - User requests the `/article/{article_id}` endpoint.
   - The backend calls the Vector Store to retrieve the article.
   - The backend calls the News Recommender to generate a summary for the article.
   - The backend returns the article and summary as JSON.

## Configuration

The application is configured using environment variables and configuration files:

- `config.py`: Contains configuration variables for the application.
- Environment variables: API keys and other sensitive information.

## Dependencies

The application relies on the following external services and libraries:

- **FastAPI**: Web framework for building APIs.
- **Jinja2**: Template engine for rendering HTML.
- **feedparser**: Library for parsing RSS feeds.
- **BeautifulSoup**: Library for parsing HTML.
- **Cohere**: API for generating embeddings.
- **Pinecone**: Vector database for storing and retrieving embeddings.
- **Groq**: API for generating insights and summaries.

## File Structure

```
ds_task_ai_news/
├── backend/
│   ├── main.py
│   ├── news_fetcher.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── recommender.py
│   ├── config.py
│   └── templates/
│       ├── base.html
│       ├── home.html
│       ├── news.html
│       └── recommendations.html
├── data/
│   ├── raw_news/
│   └── processed_news/
├── docs/
│   ├── API_Documentation.md
│   └── Technical_Documentation.md
└── requirements.txt
```

## Error Handling

The application uses try-except blocks to handle errors gracefully. Errors are logged using the `logging` module and returned as HTTP responses with appropriate status codes.

## Future Improvements

Potential improvements for the application include:

1. **Authentication**: Add user authentication to protect sensitive endpoints.
2. **Rate Limiting**: Implement rate limiting to prevent abuse.
3. **Caching**: Add caching to improve performance.
4. **Testing**: Add unit and integration tests.
5. **Deployment**: Deploy the application to a cloud provider.
6. **Monitoring**: Add monitoring and alerting.
7. **User Preferences**: Allow users to customize their news preferences.
8. **Mobile App**: Develop a mobile app for the application. 