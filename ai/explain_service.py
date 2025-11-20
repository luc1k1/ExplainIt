import json
from ai.prompts import PROMPT
from ai.model_client import generate
from ai.schemas import ExplainRequest, ExplainResponse

def explain_text(req: ExplainRequest) -> ExplainResponse:
    prompt = PROMPT.replace("{TEXT}", req.text)
    raw_output = generate(prompt)

    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError:
        # Если модель вернула текст, а не JSON
        data = {
            "definition": raw_output,
            "steps": [],
            "example": ""
        }

    return ExplainResponse(
        definition=data.get("definition", ""),
        steps=data.get("steps", []),
        example=data.get("example", "")
    )