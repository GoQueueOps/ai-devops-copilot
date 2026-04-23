import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.document_ingester import ingest_pdf, ingest_text_file, list_ingested_docs

router = APIRouter()

DOCS_PATH = os.path.normpath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'data', 'documents'
))

ALLOWED_EXTENSIONS = ['.pdf', '.txt', '.md']

@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    os.makedirs(DOCS_PATH, exist_ok=True)

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed: {ALLOWED_EXTENSIONS}"
        )

    filepath = os.path.join(DOCS_PATH, file.filename)

    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        doc_name = file.filename.replace('.', '_')
        if ext == '.pdf':
            chunks = ingest_pdf(filepath, doc_name)
        else:
            chunks = ingest_text_file(filepath, doc_name)

        return {
            "message": f"{file.filename} ingested successfully",
            "chunks": chunks,
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents")
def list_documents():
    os.makedirs(DOCS_PATH, exist_ok=True)
    files = [f for f in os.listdir(DOCS_PATH)
             if os.path.splitext(f)[1].lower() in ALLOWED_EXTENSIONS]
    ingested = list_ingested_docs()
    return {
        "uploaded_files": files,
        "ingested_sources": ingested,
        "count": len(files)
    }