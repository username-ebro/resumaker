"""Conversation routes"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from app.services.conversation_service import conversation_service
from app.services.transcription_service import transcription_service
from app.services.knowledge_extraction_service import knowledge_extraction_service
from app.services.knowledge_graph_service import knowledge_graph_service
from app.utils.user_utils import ensure_user_profile
import os
import uuid

router = APIRouter(prefix="/conversation", tags=["conversation"])

TEMP_AUDIO_DIR = "temp_audio"
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)

class ConversationStartRequest(BaseModel):
    user_id: str

class ConversationContinueRequest(BaseModel):
    conversation_id: str
    user_response: str
    conversation_history: list

class ConversationEndRequest(BaseModel):
    conversation_id: str
    user_id: str
    conversation_history: list

@router.post("/start")
async def start_conversation(request: ConversationStartRequest):
    """Start a new AI conversation for resume building"""

    try:
        # Ensure user profile exists
        await ensure_user_profile(request.user_id)

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

@router.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """Transcribe audio file to text using Gemini"""

    # Save audio temporarily
    file_id = str(uuid.uuid4())
    file_ext = os.path.splitext(audio.filename)[1] or '.webm'
    file_path = os.path.join(TEMP_AUDIO_DIR, f"{file_id}{file_ext}")

    try:
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await audio.read()
            f.write(content)

        print(f"Audio file saved: {file_path}, size: {os.path.getsize(file_path)} bytes")

        # Transcribe using Gemini
        transcript = await transcription_service.transcribe_audio(file_path)

        print(f"Transcription successful: {transcript[:100]}...")

        return {
            "success": True,
            "transcript": transcript
        }

    except Exception as e:
        print(f"Transcription error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

    finally:
        # Cleanup temp file
        if os.path.exists(file_path):
            os.remove(file_path)

@router.post("/end")
async def end_conversation(request: ConversationEndRequest):
    """
    End conversation and trigger knowledge extraction

    This endpoint:
    1. Takes full conversation history
    2. Extracts structured knowledge using Claude
    3. Stores entities as unconfirmed in database
    4. Returns extraction results for user confirmation

    The frontend should then navigate user to knowledge confirmation screen.
    """
    try:
        print(f"Ending conversation {request.conversation_id} for user {request.user_id}")
        print(f"Extracting knowledge from {len(request.conversation_history)} messages")

        # Extract knowledge from conversation
        extraction_result = await knowledge_extraction_service.extract_from_conversation(
            conversation_history=request.conversation_history,
            user_id=request.user_id,
            source_reference=request.conversation_id
        )

        if not extraction_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Knowledge extraction failed: {extraction_result.get('error', 'Unknown error')}"
            )

        entities = extraction_result["entities"]
        relationships = extraction_result["relationships"]

        # Store entities in database
        storage_result = await knowledge_graph_service.store_entities(
            entities=entities,
            user_id=request.user_id
        )

        if not storage_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Storage failed: {storage_result.get('error', 'Unknown error')}"
            )

        # Create relationships
        entity_ids = storage_result["entity_ids"]
        if relationships:
            await knowledge_graph_service.create_relationships(
                relationships=relationships,
                entity_ids=entity_ids
            )

        print(f"Successfully extracted and stored {len(entities)} entities")

        return {
            "success": True,
            "conversation_id": request.conversation_id,
            "facts_extracted": len(entities),
            "pending_confirmation": len(entities),
            "duplicates_removed": extraction_result.get("duplicates_removed", 0),
            "entities": entities,
            "entity_ids": entity_ids,
            "message": "Conversation ended. Please review and confirm extracted facts."
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error ending conversation: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to end conversation: {str(e)}")
