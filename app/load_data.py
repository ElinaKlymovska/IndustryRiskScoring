import json

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def integrate_data(news_file, tweets_file, output_file):
    news_data = load_json(news_file)
    tweets_data = load_json(tweets_file)

    integrated_data = []

    for news in news_data:
        integrated_data.append({
            'source': 'news',
            'title': news.get('title', ''),
            'description': news.get('description', ''),
            'content': news.get('content', ''),
            'url': news.get('url', ''),
            'published_at': news.get('published_at', '')
        })

    for tweet in tweets_data:
        integrated_data.append({
            'source': 'twitter',
            'title': '',
            'description': '',
            'content': tweet.get('text', ''),
            'url': '',
            'published_at': tweet.get('date', '')
        })

    save_json(integrated_data, output_file)
    print(f"Integrated data saved to {output_file}.")

if __name__ == "__main__":
    news_file = '../data/news/news_data.json'
    tweets_file = '../data/tweets/tweets_data.json'
    output_file = '../data/output/integrated_data.json'

    integrate_data(news_file, tweets_file, output_file)
