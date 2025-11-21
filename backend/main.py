import logging
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from ai.explain_service import explain_text
from ai.schemas import ExplainRequest, ExplainResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Explanation Service",
    description="API for simplifying complex texts using Gemini AI",
    version="1.0.0"
)

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "AI Explanation Service"}


@app.post("/explain", response_model=ExplainResponse)
async def explain(request: Request):
    """
    Explain complex text using AI.
    
    Accepts plain text in POST body and returns structured explanation
    with title and mini-outline.
    """
    try:
        # Pull raw bytes from the POST body and decode to string
        text_bytes = await request.body()
        
        if not text_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Request body cannot be empty"
            )
        
        try:
            text_str = text_bytes.decode("utf-8").strip()
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid encoding. Please use UTF-8"
            )
        
        if not text_str:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        
        # Validate and create request
        try:
            explain_request = ExplainRequest(text=text_str)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        
        # Generate explanation
        try:
            explain_response = explain_text(explain_request)
        except Exception as e:
            logger.error(f"Error in explain_text: {str(e)}", exc_info=True)
            error_detail = str(e)
            # In development, show actual error; in production, use generic message
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate explanation: {error_detail}"
            )
        
        return explain_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )