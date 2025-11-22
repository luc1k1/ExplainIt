from pydantic import BaseModel, Field, field_validator


class ExplainRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Text to explain")
    context: str = Field(default="", max_length=500, description="Optional context")

    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Text cannot be empty")
        return v.strip()


class ExplainResponse(BaseModel):
    title: str = Field(..., description="Short title (2-5 words)")
    text: str = Field(..., description="Mini-outline with example explanation")