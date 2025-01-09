# Industry Risk Scoring (Early Warning System)

## Опис проєкту
Цей додаток оцінює сектори ринку на основі аналізу неструктурованих даних (новини, звіти, соціальні медіа) для виявлення потенціалу зростання чи ризику спаду. 

### Ключові можливості:
- Збір даних із зовнішніх джерел.
- Аналіз текстових даних за допомогою Amazon Bedrock.
- Інтерактивні інтерфейси на основі Streamlit та Gradio.
- Інтеграція з AWS для автоматизації збору та обробки даних.

## Використані технології
- **Amazon Web Services (AWS)**: Збір даних, обробка та зберігання.
- **Generative AI - Bedrock**: Аналіз текстових даних.
- **Streamlit**: Візуалізація результатів.
- **Gradio**: Інтерактивний інтерфейс.
- **RAG with LangChain**: Пошук відповідей із використанням моделей штучного інтелекту.

## Встановлення та налаштування
1. Клонувати репозиторій:
   ```bash
   git clone <repository_url>

2. Встановити залежності:
   ```bash
   pip install -r requirements.txt

3. Configure environment variables: 

Create a .env file in the project root with the following:
   
         OPENAI_API_KEY =""
         NEWS_API_KEY = ''
         # Twitter API Keys
         Twitter_API_KEY = ''
         Twitter_API_KEY_SECRET = ''
         Twitter_ACCESS_TOKEN = ''
         Twitter_ACCESS_TOKEN_SECRET = ''
         Twitter_BEARER_TOKEN = ''
Create a .aws directory and create a credentials file in the project root with the following:
            
         aws_access_key_id = ''
         aws_secret_access_key = ''

4. Запустити додаток:
   ```bash
   streamlit run main.py
   

