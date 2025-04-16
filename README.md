# DS Task AI News

An AI-powered news application that fetches, processes, and recommends news articles based on your interests.

## Overview

DS Task AI News is a web application that uses AI technologies to fetch, analyze, and recommend news articles. The application fetches news from various RSS feeds, processes them using AI, and provides personalized insights and recommendations.

## Features

- **Latest News**: View the latest news articles fetched from various RSS feeds.
- **News Recommendations**: Get personalized news recommendations based on your interests.
- **AI Insights**: Receive AI-generated insights about news articles.
- **Article Summaries**: Get concise summaries of individual articles.

## Technologies Used

- **FastAPI**: Web framework for building APIs.
- **Jinja2**: Template engine for rendering HTML.
- **Tailwind CSS**: Utility-first CSS framework for styling.
- **feedparser**: Library for parsing RSS feeds.
- **BeautifulSoup**: Library for parsing HTML.
- **Cohere**: API for generating embeddings.
- **Pinecone**: Vector database for storing and retrieving embeddings.
- **Groq**: API for generating insights and summaries.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ds_task_ai_news.git
   cd ds_task_ai_news
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the required environment variables:
   - Create a `.env` file in the root directory with the following content:
     ```
     GROQ_API_KEY=your_groq_api_key
     PINECONE_API_KEY=your_pinecone_api_key
     PINECONE_ENVIRONMENT=your_pinecone_environment
     PINECONE_INDEX=your_pinecone_index
     ```

4. Run the application:
   ```   python backend/main.py
   ```

5. Open your web browser and navigate to `http://localhost:8000`.

## Documentation

- [API Documentation](docs/API_Documentation.md): Detailed documentation of the API endpoints.
- [Technical Documentation](docs/Technical_Documentation.md): Technical details of the application architecture and components.
- [User Guide](docs/User_Guide.md): Guide for using the application.

## Project Structure

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
│   ├── Technical_Documentation.md
│   └── User_Guide.md
└── requirements.txt
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Cohere](https://cohere.ai/)
- [Pinecone](https://www.pinecone.io/)
- [Groq](https://groq.com/)

