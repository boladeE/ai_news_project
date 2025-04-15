# DS Task AI News - User Guide

## Introduction

DS Task AI News is an AI-powered news application that fetches, processes, and recommends news articles based on your interests. The application uses advanced AI technologies to analyze news articles and provide personalized insights and recommendations.

## Features

- **Latest News**: View the latest news articles fetched from various RSS feeds.
- **News Recommendations**: Get personalized news recommendations based on your interests.
- **AI Insights**: Receive AI-generated insights about news articles.
- **Article Summaries**: Get concise summaries of individual articles.

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
   ```
   python backend/main.py
   ```

5. Open your web browser and navigate to `http://localhost:8000`.

## Using the Application

### Home Page

The home page provides links to the main features of the application:

- **Latest News**: View the latest news articles.
- **Technology News**: Get recommendations for technology-related news.
- **AI News**: Get recommendations for AI-related news.

### Latest News

To view the latest news articles:

1. Click on the "View Latest News" button on the home page.
2. The application will fetch the latest news articles from the configured RSS feeds.
3. The articles will be displayed in a grid layout with the following information:
   - Title
   - Content preview
   - Source
   - Publication date
   - Categories
   - "Read More" button

### News Recommendations

To get personalized news recommendations:

1. Click on one of the recommendation buttons on the home page (e.g., "Technology News" or "AI News").
2. Alternatively, you can navigate to `/recommend-news?query=your_search_query` to get recommendations based on a specific query.
3. The application will display recommended articles and AI-generated insights.
4. The insights section includes:
   - Themes: Main topics and areas of focus in the news articles.
   - Key Insights: Key takeaways and observations from the articles.
   - Implications: Potential consequences and outcomes of the trends and developments.
   - Related Areas: Other areas of interest connected to the themes and insights.

### Article Details

To view the details of a specific article:

1. Click on the "Read More" button for an article.
2. The article will open in a new tab with the full content.

## Customization

### Adding RSS Feeds

To add or modify the RSS feeds:

1. Open the `backend/config.py` file.
2. Locate the `RSS_FEEDS` list.
3. Add or remove RSS feed URLs as needed.

### Changing the UI

The application uses Tailwind CSS for styling. To modify the UI:

1. Open the HTML templates in the `backend/templates` directory.
2. Modify the HTML and CSS classes as needed.

## Troubleshooting

### Common Issues

1. **Application not starting**:
   - Check if all dependencies are installed correctly.
   - Verify that the environment variables are set correctly.
   - Check the console for error messages.

2. **No news articles displayed**:
   - Check your internet connection.
   - Verify that the RSS feeds are accessible.
   - Check the console for error messages.

3. **AI insights not displaying correctly**:
   - Verify that the Groq API key is set correctly.
   - Check the console for error messages.

### Getting Help

If you encounter any issues not covered in this guide, please:

1. Check the console for error messages.
2. Refer to the API and Technical documentation.
3. Contact the development team for assistance.

## Conclusion

DS Task AI News is a powerful tool for staying informed about the latest news and trends. By leveraging AI technologies, it provides personalized insights and recommendations to help you make sense of the news.

We hope you find this guide helpful. If you have any questions or feedback, please don't hesitate to contact us. 