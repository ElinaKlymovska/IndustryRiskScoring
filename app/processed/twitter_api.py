import os

import tweepy
import json
from dotenv import load_dotenv

load_dotenv()

# Twitter API Keys
API_KEY = os.getenv("Twitter_API_KEY")
API_KEY_SECRET = os.getenv("Twitter_API_KEY_SECRET")
ACCESS_TOKEN =  os.getenv("Twitter_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("Twitter_ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("Twitter_BEARER_TOKEN")

# Authenticate with Twitter API v2
client = tweepy.Client(bearer_token=BEARER_TOKEN)

def save_tweets_to_file(tweets, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False, indent=4)

def fetch_tweets_v2(keywords, count=100, output_file='../../data/tweets/tweets_data.json'):
    try:
        query = f"{keywords} -is:retweet"  # Виключаємо ретвіти
        response = client.search_recent_tweets(query=query, max_results=count,
                                               tweet_fields=['created_at', 'author_id', 'text'])

        tweets_data = []
        for tweet in response.data:
            tweets_data.append({
                'date': tweet.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'author_id': tweet.author_id,
                'text': tweet.text
            })

        save_tweets_to_file(tweets_data, output_file)
        print(f"Fetched and saved {len(tweets_data)} tweets to {output_file}.")

        return tweets_data

    except Exception as e:
        print(f"Error fetching tweets: {e}")

# test
if __name__ == "__main__":
    keywords = "finance OR technology"
    tweets = fetch_tweets_v2(keywords)
