import os
from dotenv import load_dotenv

# Keep the API key in an environment variable so it never ends up in git
load_dotenv()

GEMINI_API_KEY = os.getenv('GENAI_API_KEY')
MODEL_NAME = "gemini-2.5-flash"
DEFAULT_TEMPERATURE = 0.4
MAX_OUTPUT_TOKENS = 500