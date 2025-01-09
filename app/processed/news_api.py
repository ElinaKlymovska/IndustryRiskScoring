import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_NEWS_KEY')
URL = 'https://newsapi.org/v2/everything'

def clean_text(text):
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^A-Za-z0-9 .,!?\']+', '', text)
    return text.strip()

def fetch_news(keywords, language='en', sort_by='publishedAt', page_size=100):
    params = {
        'q': keywords,
        'language': language,
        'sortBy': sort_by,
        'pageSize': page_size,
        'apiKey': API_KEY
    }

    try:
        response = requests.get(URL, params=params)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])

            cleaned_articles = []
            for article in articles:
                cleaned_articles.append({
                    'title': clean_text(article.get('title', '')),
                    'description': clean_text(article.get('description', '')),
                    'content': clean_text(article.get('content', '')),
                    'url': article.get('url', ''),
                    'published_at': article.get('publishedAt', '')
                })

            with open('../../data/news/news_data.json', 'w', encoding='utf-8') as f:
                json.dump(cleaned_articles, f, ensure_ascii=False, indent=4)

            print(f"Fetched and saved {len(cleaned_articles)} articles.")
        else:
            print(f"Error: {response.status_code}, {response.text}")

    except Exception as e:
        print(f"Error fetching news: {e}")

if __name__ == "__main__":
    keywords = "finance OR technology"
    fetch_news(keywords)
