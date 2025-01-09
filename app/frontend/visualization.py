import matplotlib.pyplot as plt

def visualize_results(correlations):
    """Візуалізація кореляцій між подіями та оцінками настроїв."""
    events = [item['event'] for item in correlations]
    sentiments = [item['sentiment_score'] for item in correlations]

    plt.figure(figsize=(12, 6))
    plt.bar(events, sentiments, color='skyblue')
    plt.xlabel('Події')
    plt.ylabel('Оцінка настрою')
    plt.title('Кореляція подій та настрою з крипторинком')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
