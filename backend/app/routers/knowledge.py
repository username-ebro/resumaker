"""
Knowledge Router
API endpoints for knowledge graph management (extraction, confirmation, editing)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.services.knowledge_extraction_service import knowledge_extraction_service
from app.services.knowledge_graph_service import knowledge_graph_service
from app.database import get_supabase

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


# Pydantic models
class ExtractConversationRequest(BaseModel):
    user_id: str
    conversation_history: List[Dict[str, str]]
    source_reference: Optional[str] = None


class ExtractResumeRequest(BaseModel):
    user_id: str
    resume_text: str
    source_reference: Optional[str] = None


class ConfirmEntitiesRequest(BaseModel):
    user_id: str
    entity_ids: List[str]


class UpdateEntityRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    entity_type: Optional[str] = None
    confidence_score: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_current: Optional[bool] = None
    structured_data: Optional[Dict[str, Any]] = None


@router.post("/extract-conversation")
async def extract_from_conversation(request: ExtractConversationRequest):
    """
    Extract knowledge entities from conversation history

    This endpoint:
    1. Takes conversation messages
    2. Uses Claude to extract structured facts
    3. Stores entities as unconfirmed in database
    4. Returns extracted entities for user review
    """
    try:
        print(f"Extracting knowledge from conversation for user {request.user_id}")

        # Extract entities using AI
        extraction_result = await knowledge_extraction_service.extract_from_conversation(
            conversation_history=request.conversation_history,
            user_id=request.user_id,
            source_reference=request.source_reference
        )

        if not extraction_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Extraction failed: {extraction_result.get('error', 'Unknown error')}"
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

        print(f"Successfully extracted {len(entities)} entities from conversation")

        return {
            "success": True,
            "entities": entities,
            "relationships": relationships,
            "total_extracted": len(entities),
            "duplicates_removed": extraction_result.get("duplicates_removed", 0),
            "entity_ids": entity_ids
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Conversation extraction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@router.post("/extract-resume")
async def extract_from_resume(request: ExtractResumeRequest):
    """
    Extract knowledge entities from resume text

    This endpoint:
    1. Takes raw resume text (from OCR or paste)
    2. Uses Claude to extract structured facts
    3. Stores entities as unconfirmed in database
    4. Returns extracted entities for user review
    """
    try:
        print(f"Extracting knowledge from resume for user {request.user_id}")

        # Extract entities using AI
        extraction_result = await knowledge_extraction_service.extract_from_resume(
            resume_text=request.resume_text,
            user_id=request.user_id,
            source_reference=request.source_reference
        )

        if not extraction_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Extraction failed: {extraction_result.get('error', 'Unknown error')}"
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

        print(f"Successfully extracted {len(entities)} entities from resume")

        return {
            "success": True,
            "entities": entities,
            "relationships": relationships,
            "total_extracted": len(entities),
            "duplicates_removed": extraction_result.get("duplicates_removed", 0),
            "entity_ids": entity_ids
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Resume extraction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@router.get("/pending/{user_id}")
async def get_pending_entities(user_id: str):
    """
    Get all unconfirmed entities for user

    Returns:
    - All pending entities
    - Grouped by type (jobs, skills, projects, etc.)
    - Hierarchical structure (jobs with nested details)
    - Total count
    """
    try:
        print(f"Fetching pending entities for user {user_id}")

        result = await knowledge_graph_service.get_pending_entities(user_id)

        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch entities: {result.get('error', 'Unknown error')}"
            )

        return {
            "success": True,
            "total_pending": result["total_pending"],
            "entities": result["entities"],
            "grouped_by_type": result["grouped_by_type"],
            "hierarchical": result["hierarchical"]
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching pending entities: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch entities: {str(e)}")


@router.get("/confirmed/{user_id}")
async def get_confirmed_entities(user_id: str):
    """
    Get all confirmed entities for user (their complete knowledge graph)

    Returns:
    - All confirmed entities
    - Relationships between entities
    - Grouped by type
    - Summary statistics
    """
    try:
        print(f"Fetching confirmed entities for user {user_id}")

        result = await knowledge_graph_service.get_user_knowledge_graph(
            user_id=user_id,
            confirmed_only=True
        )

        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch knowledge graph: {result.get('error', 'Unknown error')}"
            )

        return {
            "success": True,
            "total_entities": result["total_entities"],
            "entities": result["entities"],
            "relationships": result["relationships"],
            "grouped_by_type": result["grouped_by_type"],
            "hierarchical": result["hierarchical"],
            "summary": result["summary"]
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching confirmed entities: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch entities: {str(e)}")


@router.post("/confirm")
async def confirm_entities(request: ConfirmEntitiesRequest):
    """
    Mark entities as confirmed by user

    This is called after user reviews extracted facts and clicks "Confirm All" or
    confirms individual items. Confirmed entities become part of their knowledge base
    and can be used in resume generation.
    """
    try:
        print(f"Confirming {len(request.entity_ids)} entities for user {request.user_id}")

        if not request.entity_ids:
            return {
                "success": True,
                "confirmed_count": 0,
                "message": "No entities provided"
            }

        result = await knowledge_graph_service.confirm_entities(
            entity_ids=request.entity_ids,
            user_id=request.user_id
        )

        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Confirmation failed: {result.get('error', 'Unknown error')}"
            )

        print(f"Successfully confirmed {result['confirmed_count']} entities")

        return {
            "success": True,
            "confirmed_count": result["confirmed_count"]
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error confirming entities: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Confirmation failed: {str(e)}")


@router.put("/entity/{entity_id}")
async def update_entity(
    entity_id: str,
    user_id: str,
    request: UpdateEntityRequest
):
    """
    Update an entity (when user edits before confirming)

    Query params:
    - user_id: For security validation

    Body can include any entity fields:
    - title, description, entity_type
    - confidence_score, start_date, end_date, is_current
    - structured_data (full object)
    """
    try:
        print(f"Updating entity {entity_id} for user {user_id}")

        # Build updates dict from request (only include provided fields)
        updates = {}
        if request.title is not None:
            updates["title"] = request.title
        if request.description is not None:
            updates["description"] = request.description
        if request.entity_type is not None:
            updates["entity_type"] = request.entity_type
        if request.confidence_score is not None:
            # Validate confidence score
            if request.confidence_score < 0.0 or request.confidence_score > 1.0:
                raise HTTPException(
                    status_code=400,
                    detail="confidence_score must be between 0.00 and 1.00"
                )
            updates["confidence_score"] = request.confidence_score
        if request.start_date is not None:
            updates["start_date"] = request.start_date
        if request.end_date is not None:
            updates["end_date"] = request.end_date
        if request.is_current is not None:
            updates["is_current"] = request.is_current
        if request.structured_data is not None:
            updates["structured_data"] = request.structured_data

        if not updates:
            raise HTTPException(
                status_code=400,
                detail="No update fields provided"
            )

        result = await knowledge_graph_service.update_entity(
            entity_id=entity_id,
            updates=updates,
            user_id=user_id
        )

        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Update failed: {result.get('error', 'Unknown error')}"
            )

        if not result["entity"]:
            raise HTTPException(
                status_code=404,
                detail="Entity not found or access denied"
            )

        print(f"Successfully updated entity {entity_id}")

        return {
            "success": True,
            "entity": result["entity"]
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating entity: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")


@router.delete("/entity/{entity_id}")
async def delete_entity(entity_id: str, user_id: str):
    """
    Delete an entity (when user rejects extracted fact)

    Query params:
    - user_id: For security validation

    This will cascade delete:
    - All child entities (e.g., job details under a job)
    - All relationships involving this entity
    """
    try:
        print(f"Deleting entity {entity_id} for user {user_id}")

        result = await knowledge_graph_service.delete_entity(
            entity_id=entity_id,
            user_id=user_id
        )

        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Deletion failed: {result.get('error', 'Unknown error')}"
            )

        print(f"Successfully deleted entity {entity_id}")

        return {
            "success": True,
            "deleted": True
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting entity: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")


@router.get("/summary/{user_id}")
async def get_knowledge_summary(user_id: str):
    """
    Get summary statistics for user's knowledge graph

    Returns:
    - Total entities (all time)
    - Confirmed vs pending counts
    - Breakdown by type (jobs, skills, projects, etc.)
    - Completeness score
    """
    try:
        print(f"Fetching knowledge summary for user {user_id}")

        # Get full knowledge graph
        result = await knowledge_graph_service.get_user_knowledge_graph(
            user_id=user_id,
            confirmed_only=False  # Include all entities for summary
        )

        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch summary: {result.get('error', 'Unknown error')}"
            )

        return {
            "success": True,
            "summary": result["summary"],
            "total_entities": result["total_entities"],
            "grouped_by_type": result["grouped_by_type"]
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching knowledge summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch summary: {str(e)}")
