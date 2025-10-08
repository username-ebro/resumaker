"""Import conversation routes"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.import_parser import import_parser

router = APIRouter(prefix="/imports", tags=["imports"])

class ImportRequest(BaseModel):
    conversation_text: str
    source_platform: str  # "chatgpt" | "claude" | "other"

@router.post("/parse")
async def parse_conversation(request: ImportRequest):
    """Parse a ChatGPT/Claude conversation and extract resume data"""

    try:
        extracted_data = await import_parser.parse_conversation(
            request.conversation_text,
            request.source_platform
        )

        return {
            "success": True,
            "source": request.source_platform,
            "extracted_data": extracted_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing failed: {str(e)}")
