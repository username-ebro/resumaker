"""File upload and OCR routes"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ocr_service import ocr_service
import os
import uuid

router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload resume (PDF/Image) and extract data via OCR"""

    # Validate file type
    allowed_types = ['application/pdf', 'image/jpeg', 'image/png']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, JPG, PNG allowed.")

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

        return {
            "success": True,
            "file_id": file_id,
            "file_name": file.filename,
            "extracted_data": extracted_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")

    finally:
        # Cleanup temp file
        if os.path.exists(file_path):
            os.remove(file_path)
