# DS Task AI News API Documentation

## Overview

The DS Task AI News API is a FastAPI-based application that provides endpoints for fetching, processing, and recommending news articles. The API uses AI-powered analysis to generate insights and recommendations based on news articles from various RSS feeds.

## Base URL

```
http://localhost:8000
```

## Endpoints

### 1. Home Page

**Endpoint:** `/`

**Method:** `GET`

**Description:** Returns the home page with links to other routes.

**Response:** HTML page with navigation links to other endpoints.

**Example:**
```
GET /
```

### 2. Fetch News

**Endpoint:** `/fetch-news`

**Method:** `GET`

**Description:** Fetches news from RSS feeds, processes them, and stores them in the vector database. Returns a page displaying the latest news articles.

**Response:** HTML page displaying the latest news articles.

**Example:**
```
GET /fetch-news
```

### 3. Recommend News

**Endpoint:** `/recommend-news`

**Method:** `GET`

**Description:** Gets news recommendations based on an article ID or search query. Returns a page displaying recommended articles and AI-generated insights.

**Query Parameters:**
- `article_id` (optional): ID of an article to base recommendations on.
- `query` (optional): Search query to base recommendations on.

**Response:** HTML page displaying recommended articles and AI-generated insights.

**Example:**
```
GET /recommend-news?query=artificial%20intelligence
```

### 4. Get Article

**Endpoint:** `/article/{article_id}`

**Method:** `GET`

**Description:** Gets a specific article and its summary.

**Path Parameters:**
- `article_id`: ID of the article to retrieve.

**Response:** JSON object containing the article and its summary.

**Example Response:**
```json
{
  "article": {
    "title": "Example Article Title",
    "content": "Example article content...",
    "link": "https://example.com/article",
    "published": "2023-01-01T12:00:00",
    "source": "Example News",
    "categories": ["Technology", "AI"],
    "id": "article123"
  },
  "summary": "This is a summary of the article..."
}
```

**Example:**
```
GET /article/article123
```

## Data Models

### Article

```json
{
  "title": "string",
  "content": "string",
  "link": "string",
  "published": "string",
  "source": "string",
  "categories": ["string"],
  "id": "string"
}
```

### Insights

```json
{
  "themes": ["string"],
  "insights": ["string"],
  "implications": ["string"],
  "related_areas": ["string"]
}
```

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests:

- `200 OK`: The request was successful.
- `400 Bad Request`: The request was invalid or cannot be served.
- `404 Not Found`: The requested resource was not found.
- `500 Internal Server Error`: An error occurred on the server.

Error responses include a JSON object with a `detail` field containing a description of the error:

```json
{
  "detail": "Error message"
}
```

## Authentication

The API does not currently require authentication.

## Rate Limiting

The API does not currently implement rate limiting.

## Dependencies

The API relies on the following external services:

- **Groq API**: For generating article summaries and insights.
- **Pinecone Vector Database**: For storing and retrieving article embeddings.

## Configuration

The API can be configured by modifying the following environment variables:

- `GROQ_API_KEY`: API key for the Groq service.
- `PINECONE_API_KEY`: API key for the Pinecone vector database.
- `PINECONE_ENVIRONMENT`: Environment for the Pinecone vector database.
- `PINECONE_INDEX`: Index name for the Pinecone vector database.

## Development

To run the API locally:

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set the required environment variables.

3. Run the API:
   ```
   python backend/main.py
   ```

The API will be available at `http://localhost:8000`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
