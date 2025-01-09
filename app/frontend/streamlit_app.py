import streamlit as st
import json

from app.frontend.visualization import visualize_results
from app.text_preprocessing import analyze_sentiment_and_correlations_with_state_graph

# Заголовок додатку
st.title("Аналіз впливу подій на криптовалютний ринок")

# Автоматичне завантаження основних даних
def load_default_data():
    try:
        with open('../data/news/news_data.json', 'r') as news_file, open('../data/tweets/tweets_data.json', 'r') as twitter_file:
            news_data = json.load(news_file)
            twitter_data = json.load(twitter_file)
        return news_data, twitter_data
    except FileNotFoundError:
        st.error("Основні дані не знайдені. Переконайтеся, що файли знаходяться у відповідній директорії.")
        return [], []

news_data, twitter_data = load_default_data()

# Відображення оброблених основних даних
st.subheader("Основні дані")
st.write("Загальна кількість новин: ", len(news_data))
st.write("Загальна кількість твітів: ", len(twitter_data))

# Додаткові дані від користувача
st.subheader("Додаткові дані для аналізу")
user_input = st.text_area("Додайте текст подій або опис, які впливають на ринок:", "")
uploaded_file = st.file_uploader("Завантажте текстовий файл для аналізу (за бажанням):", type=['txt'])

# Обробка додаткових даних
def process_additional_data():
    additional_data = []
    if user_input:
        additional_data.append(user_input)
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        additional_data.append(content)
    return additional_data

additional_data = process_additional_data()

# Комбінування основних і додаткових даних
combined_data = news_data + twitter_data + additional_data

# Аналіз даних
if st.button("Запустити аналіз"):
    st.subheader("Результати аналізу")
    with st.spinner("Обробка даних та проведення аналізу..."):
        correlations = analyze_sentiment_and_correlations_with_state_graph(combined_data)
        st.success("Аналіз завершено!")

        # Візуалізація результатів
        visualize_results(correlations)

        # Відображення змін
        st.subheader("Виявлені кореляції")
        for correlation in correlations:
            st.write(f"Подія: {correlation['event']}, Оцінка настрою: {correlation['analysis']['sentiment_score']}")

st.sidebar.title("Налаштування")
st.sidebar.write("Цей додаток аналізує вплив соціальних, політичних та економічних подій на крипторинок. Ви можете додати додаткові дані для перевірки їх впливу.")
