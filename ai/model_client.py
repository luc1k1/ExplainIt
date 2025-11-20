from google import genai
from ai.config import GEMINI_API_KEY, MODEL_NAME

client = genai.Client(api_key=GEMINI_API_KEY)

def generate(prompt: str):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[prompt]
    )
    return response.text