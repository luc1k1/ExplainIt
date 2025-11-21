import json
import re
import logging
from ai.prompts import PROMPT
from ai.model_client import generate
from ai.schemas import ExplainRequest, ExplainResponse

logger = logging.getLogger(__name__)

def clean_json_output(text: str) -> str:
    """Remove markdown code blocks and extract clean JSON"""
    # Remove markdown code blocks (```json ... ```)
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text

def explain_text(req: ExplainRequest) -> ExplainResponse:
    """
    Generate explanation for the given text using AI.
    
    Args:
        req: ExplainRequest with text to explain
        
    Returns:
        ExplainResponse with title and text explanation
    """
    logger.info(f"Generating explanation for text (length: {len(req.text)})")
    
    prompt = PROMPT.replace("{TEXT}", req.text)
    raw_output = generate(prompt)
    
    # Clean the output from markdown blocks
    cleaned_output = clean_json_output(raw_output)
    logger.debug(f"Cleaned output length: {len(cleaned_output)}")

    try:
        data = json.loads(cleaned_output)
        
        # Handle nested JSON structure if model returns it
        if "text" in data and isinstance(data["text"], dict):
            #           extract text from nested structure
            nested = data["text"]
            if "outline" in nested and isinstance(nested["outline"], list):
                # Build plain text from outline points
                text_parts = []
                for item in nested["outline"]:
                    if isinstance(item, dict):
                        point = item.get("point", "")
                        explanation = item.get("explanation", "")
                        text_parts.append(f"• {point}: {explanation}")
                data["text"] = "\n\n".join(text_parts)
            else:
                # Fallback: convert nested dict to string
                data["text"] = json.dumps(nested, ensure_ascii=False, indent=2)
        
    except json.JSONDecodeError as e:
        # fallback if the model returns plain text instead of valid JSON
        logger.warning(f"Failed to parse JSON response: {str(e)}")
        # generate a simple title from the text
        title_prompt = f"Create a concise 2-5 word title for this text: {raw_output[:200]}, Answer in the same language you received the text"
        try:
            title = generate(title_prompt).strip().splitlines()[0]
        except Exception as title_error:
            logger.warning(f"Failed to generate title: {str(title_error)}")
            title = "Summary"
        data = {
            "title": title,
            "text": raw_output
        }

    return ExplainResponse(
        title=data.get("title", ""),
        text=data.get("text", "")
    )