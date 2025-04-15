from groq import Groq
from typing import List, Dict, Any
from config import GROQ_API_KEY
import json

class NewsRecommender:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def analyze_articles(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze a set of articles using Groq to generate insights."""
        try:
            # Prepare the prompt
            articles_text = "\n\n".join([
                f"Title: {article['title']}"
                for article in articles
            ])
            
            prompt = f"""Analyze these news articles and provide insights:

{articles_text}

Please provide:
1. Main themes and topics
2. Key insights and trends
3. Potential implications
4. Related areas of interest

Format the response as a JSON with these keys: themes, insights, implications, related_areas"""

            # Get completion from Groq
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a news analyst providing insights about technology and AI news."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-70b-8192",
                temperature=0.7,
                max_tokens=500
            )

            # Parse and return the analysis
            response_text = completion.choices[0].message.content
            
            # Try to extract JSON from the response if it's wrapped in markdown code blocks
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    pass
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    pass
            
            # If we couldn't extract JSON, try to parse the entire response
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                # If all parsing attempts fail, return the raw text
                return response_text
        except Exception as e:
            print(f"Error analyzing articles: {str(e)}")
            return {
                "themes": [],
                "insights": [],
                "implications": [],
                "related_areas": []
            }

    def generate_summary(self, article: Dict[str, Any]) -> str:
        """Generate a summary of a single article using Groq."""
        try:
            prompt = f"""Summarize this news article:

Title: {article['title']}
Content: {article['content']}

Please provide a concise summary focusing on the key points and implications."""

            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a news summarizer providing concise summaries of technology and AI news."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-70b-8192",
                temperature=0.5,
                max_tokens=250
            )

            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return "Unable to generate summary."
