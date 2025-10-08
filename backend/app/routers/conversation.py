"""Conversation routes"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.conversation_service import conversation_service

router = APIRouter(prefix="/conversation", tags=["conversation"])

class ConversationStartRequest(BaseModel):
    user_id: str

class ConversationContinueRequest(BaseModel):
    conversation_id: str
    user_response: str
    conversation_history: list

@router.post("/start")
async def start_conversation(request: ConversationStartRequest):
    """Start a new AI conversation for resume building"""

    try:
        result = await conversation_service.start_conversation(request.user_id)
        return {
            "success": True,
            **result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start conversation: {str(e)}")

@router.post("/continue")
async def continue_conversation(request: ConversationContinueRequest):
    """Continue the conversation and extract knowledge"""

    try:
        result = await conversation_service.continue_conversation(
            request.conversation_history,
            request.user_response
        )

        return {
            "success": True,
            **result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversation error: {str(e)}")
