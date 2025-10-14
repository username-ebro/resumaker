"""File upload and OCR routes"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.ocr_service import ocr_service
from app.services.knowledge_extraction_service import knowledge_extraction_service
from app.services.knowledge_graph_service import knowledge_graph_service
import os
import uuid

router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/resume")
async def upload_resume(
    file: UploadFile = File(...),
    user_id: str = Form(None)
):
    """
    Upload resume (PDF/Image/DOCX/DOC/TXT) and extract data via OCR

    If user_id is provided, automatically extracts knowledge entities
    and stores them as unconfirmed for user review.
    """

    # Validate file type
    allowed_types = [
        'application/pdf',
        'image/jpeg',
        'image/png',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # .docx
        'application/msword',  # .doc
        'text/plain'  # .txt
    ]

    # Also check file extension as a fallback
    allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.docx', '.doc', '.txt']
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file.content_type not in allowed_types and file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Allowed: PDF, JPG, PNG, DOCX, DOC, TXT"
        )

    # Save file temporarily
    file_id = str(uuid.uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_ext}")

    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Extract data via OCR
        extracted_data = await ocr_service.extract_resume_text(file_path)

        response = {
            "success": True,
            "file_id": file_id,
            "file_name": file.filename,
            "extracted_data": extracted_data
        }

        # If user_id provided, automatically extract knowledge
        if user_id:
            print(f"Auto-extracting knowledge from uploaded resume for user {user_id}")

            try:
                # Extract knowledge entities
                extraction_result = await knowledge_extraction_service.extract_from_resume(
                    resume_text=extracted_data,
                    user_id=user_id,
                    source_reference=file_id
                )

                if extraction_result["success"]:
                    entities = extraction_result["entities"]
                    relationships = extraction_result["relationships"]

                    # Store entities in database
                    storage_result = await knowledge_graph_service.store_entities(
                        entities=entities,
                        user_id=user_id
                    )

                    if storage_result["success"]:
                        # Create relationships
                        entity_ids = storage_result["entity_ids"]
                        if relationships:
                            await knowledge_graph_service.create_relationships(
                                relationships=relationships,
                                entity_ids=entity_ids
                            )

                        print(f"Successfully extracted {len(entities)} entities from resume")

                        # Add extraction results to response
                        response["knowledge_extraction"] = {
                            "success": True,
                            "entities_extracted": len(entities),
                            "pending_confirmation": len(entities),
                            "duplicates_removed": extraction_result.get("duplicates_removed", 0),
                            "entity_ids": entity_ids
                        }
                    else:
                        print(f"Storage failed: {storage_result.get('error')}")
                        response["knowledge_extraction"] = {
                            "success": False,
                            "error": storage_result.get("error", "Storage failed")
                        }
                else:
                    print(f"Extraction failed: {extraction_result.get('error')}")
                    response["knowledge_extraction"] = {
                        "success": False,
                        "error": extraction_result.get("error", "Extraction failed")
                    }

            except Exception as e:
                print(f"Knowledge extraction error (non-fatal): {str(e)}")
                # Don't fail the whole upload if knowledge extraction fails
                response["knowledge_extraction"] = {
                    "success": False,
                    "error": str(e)
                }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")

    finally:
        # Cleanup temp file
        if os.path.exists(file_path):
            os.remove(file_path)
