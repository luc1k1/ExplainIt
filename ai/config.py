import os
from dotenv import load_dotenv

# Храним ключ в переменной окружения
# ai/config.py
load_dotenv() # загражаю .env файл для безопастности ключа


GEMINI_API_KEY = os.getenv('GENAI_API_KEY') # ключ из .env

MODEL_NAME = "gemini-2.5-flash"  # тестовая модель
DEFAULT_TEMPERATURE = 0.4
MAX_OUTPUT_TOKENS = 500