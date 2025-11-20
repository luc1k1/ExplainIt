from fastapi import FastAPI, Request
from ai.model_client import generate

app = FastAPI()

@app.post("/explain")
async def explain(request: Request):
    # Получаем строку из POST body
    text_bytes = await request.body()
    text_str = text_bytes.decode("utf-8")

    # Генерируем summary как единый текст (не JSON)
    summary_prompt = f"Объясни этот текст простыми словами в виде одного параграфа:\n{text_str}"
    summary = generate(summary_prompt).strip()

    # Генерируем title (2–3 слова)
    title_prompt = f"Сделай краткий заголовок из 2–3 слов для этого текста: {text_str}"
    title_raw = generate(title_prompt)
    title = title_raw.splitlines()[0].strip()

    # Возвращаем JSON с чистым summary
    return {
        "title": title,
        "summary": summary
    }