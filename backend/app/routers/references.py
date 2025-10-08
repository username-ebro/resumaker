"""Reference request routes"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.reference_service import reference_service

router = APIRouter(prefix="/references", tags=["references"])

class ReferenceRequestCreate(BaseModel):
    user_id: str
    target_role: str
    reference_type: str  # "manager" | "colleague" | "client"

class ReferenceResponseSubmit(BaseModel):
    share_token: str
    reference_name: str
    reference_relationship: str
    responses: dict  # Question answers

@router.post("/create")
async def create_reference_request(request: ReferenceRequestCreate):
    """Generate a shareable reference request"""

    try:
        result = await reference_service.generate_reference_request(
            request.user_id,
            request.target_role,
            request.reference_type
        )

        return {
            "success": True,
            **result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create reference request: {str(e)}")

@router.post("/submit")
async def submit_reference_response(response: ReferenceResponseSubmit):
    """Submit a reference response (public endpoint)"""

    try:
        # Combine all responses into text
        response_text = "\n\n".join([
            f"{q}: {a}" for q, a in response.responses.items()
        ])

        # Parse and extract structured data
        parsed_data = await reference_service.parse_reference_response(response_text)

        return {
            "success": True,
            "message": "Reference submitted successfully",
            "parsed_data": parsed_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit reference: {str(e)}")
