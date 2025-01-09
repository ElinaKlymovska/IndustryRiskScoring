import boto3
import json
import time
from random import randint
import botocore.exceptions

# Конфігурація
BEDROCK_MODEL = "anthropic.claude-3-sonnet-20240229-v1:0"
ANTHROPIC_VERSION = "bedrock-2023-05-31"
REGION = "us-east-1"
MAX_RETRIES = 4
BASE_WAIT_TIME = 2

# Ініціалізація клієнта
bedrock_client = boto3.client(
    service_name='bedrock-runtime',
    region_name=REGION
)

def build_request_body(prompt_text):
    """
    Формує тіло запиту до Bedrock API.
    """
    return json.dumps({
        "anthropic_version": ANTHROPIC_VERSION,
        "messages": [
            {"role": "user", "content": prompt_text}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    })

def parse_response(response):
    """
    Парсить відповідь від моделі.
    """
    try:
        response_body = json.loads(response['body'].read().decode('utf-8'))
        if 'content' in response_body and isinstance(response_body['content'], list):
            return "".join(
                item['text'] for item in response_body['content']
                if item.get('type') == 'text' and 'text' in item
            )
        else:
            print("Unexpected response format:", response_body)
            return "Error: Unexpected response format."
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing response: {e}")
        return f"Error parsing response: {e}"

def analyze_text_with_bedrock(prompt_text):
    """
    Відправляє запит до Bedrock API з обробкою повторних спроб.
    """
    retries = 0

    while retries < MAX_RETRIES:
        try:
            body = build_request_body(prompt_text)
            response = bedrock_client.invoke_model(
                modelId=BEDROCK_MODEL,
                contentType="application/json",
                accept="*/*",
                body=body
            )
            return parse_response(response)

        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'ThrottlingException':
                retries += 1
                wait_time = BASE_WAIT_TIME * 2 ** retries + randint(0, BASE_WAIT_TIME)
                print(f"Throttling detected. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"ClientError occurred: {error}")
                return f"Error: {error}"

        except Exception as e:
            print(f"Unexpected error: {e}")
            return f"Error: {e}"

    print(f"Error: Throttling limit reached after {MAX_RETRIES} retries.")
    return f"Error: Throttling limit reached."

# Тест
if __name__ == "__main__":
    text_to_analyze = "Надай короткий зміст навчального посібника 'Фінанси' за редакцією О.Я. Стойка."
    result = analyze_text_with_bedrock(text_to_analyze)
    print(f"Result: {result}")
