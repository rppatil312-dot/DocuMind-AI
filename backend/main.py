
from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
from uuid import uuid4

from document_processor import extract_text_from_pdf

app = FastAPI(
    title="DocuMind AI",
    description="AI-powered PDF Question Answering System",
    version="1.0.0"
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Welcome to DocuMind AI!",
        "status": "Backend is running successfully"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid PDF file"
        )

    file_id = str(uuid4())
    file_path = UPLOAD_DIR / f"{file_id}.pdf"

    try:
        content = await file.read()

        if not content.startswith(b"%PDF"):
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is not a valid PDF"
            )

        file_path.write_bytes(content)

        pages = extract_text_from_pdf(str(file_path))

        return {
            "message": "PDF uploaded successfully!",
            "file_id": file_id,
            "filename": file.filename,
            "total_pages_extracted": len(pages),
            "extracted_pages": pages
        }

    except HTTPException:
        raise

    except Exception as error:
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=400,
            detail=f"PDF processing failed: {str(error)}"
        )

    finally:
        await file.close()
