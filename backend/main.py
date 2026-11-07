
from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
from uuid import uuid4

from document_processor import extract_text_from_pdf
from text_chunker import split_text_into_chunks

from embedding import (
    generate_embeddings,
    generate_query_embedding
)

from vector_store import (
    store_embeddings,
    search_similar_chunks
)


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
        # Read uploaded file
        content = await file.read()

        # Validate PDF file
        if not content.startswith(b"%PDF"):
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is not a valid PDF"
            )

        file_path.write_bytes(content)

        # Step 1: Extract text from PDF
        pages = extract_text_from_pdf(str(file_path))

        if not pages:
            raise HTTPException(
                status_code=400,
                detail="No readable text found in the PDF"
            )

        # Step 2: Split extracted text into chunks
        chunks = split_text_into_chunks(pages)

        # Step 3: Generate embeddings
        embedded_chunks = generate_embeddings(chunks)

        # Step 4: Store embeddings in ChromaDB
        stored_count = store_embeddings(embedded_chunks, file_id)

        return {
            "message": "PDF uploaded and stored successfully!",
            "file_id": file_id,
            "filename": file.filename,
            "total_pages_extracted": len(pages),
            "total_chunks": len(chunks),
            "total_embeddings": len(embedded_chunks),
            "total_stored_in_vector_db": stored_count,
            "chunks": chunks
        }

    except HTTPException:
        raise

    except Exception as error:
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"PDF processing failed: {str(error)}"
        )

    finally:
        await file.close()


# Search relevant PDF content
@app.get("/search/{file_id}")
def search_pdf(file_id: str, question: str):

    try:
        # Step 1: Convert question into embedding
        query_embedding = generate_query_embedding(question)

        # Step 2: Search relevant PDF chunks
        results = search_similar_chunks(
            query_embedding=query_embedding,
            file_id=file_id,
            n_results=3
        )

        if not results:
            return {
                "message": "No relevant information found.",
                "results": []
            }

        return {
            "file_id": file_id,
            "question": question,
            "total_results": len(results),
            "results": results
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(error)}"
        )
