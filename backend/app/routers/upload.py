from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from pathlib import Path
import os
import uuid
from datetime import datetime

from app.core.security import require_admin

router = APIRouter(prefix="/upload", tags=["Upload"])

# Upload directory (place uploads under the backend folder so StaticFiles mount matches)
UPLOAD_DIR = Path(__file__).parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Allowed extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/image", dependencies=[Depends(require_admin)])
async def upload_image(file: UploadFile = File(...)):
    """Upload an image file and return its URL path."""
    try:
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"فرمت فایل پشتیبانی نشده است. فرمت‌های مجاز: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # Check file size
        file_content = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"اندازه فایل بیش از حد است. حداکثر: {MAX_FILE_SIZE / (1024*1024)}MB"
            )

        # Generate unique filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        original_name = Path(file.filename).stem
        filename = f"{timestamp}_{unique_id}_{original_name}{file_ext}"

        # Save file
        file_path = UPLOAD_DIR / filename
        with open(file_path, "wb") as f:
            f.write(file_content)

        # Return URL path (relative to public access)
        url_path = f"/uploads/{filename}"
        
        return {
            "success": True,
            "url": url_path,
            "filename": filename,
            "size": len(file_content)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در آپلود فایل: {str(e)}"
        )
