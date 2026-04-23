import os
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'documents')
VECTORDB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'vectordb')

openai_ef = OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-ada-002"
)

chroma_client = chromadb.PersistentClient(path=os.path.normpath(VECTORDB_PATH))
collection = chroma_client.get_or_create_collection(
    name="documents",
    embedding_function=openai_ef
)

def chunk_text(text: str, chunk_size: int = 500) -> list:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def ingest_text_file(filepath: str, doc_name: str):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        collection.upsert(
            documents=[chunk],
            ids=[f"{doc_name}_chunk_{i}"],
            metadatas=[{"source": doc_name, "chunk": i}]
        )
    print(f"Ingested {len(chunks)} chunks from {doc_name}")
    return len(chunks)

def ingest_pdf(filepath: str, doc_name: str):
    from pypdf import PdfReader
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        collection.upsert(
            documents=[chunk],
            ids=[f"{doc_name}_chunk_{i}"],
            metadatas=[{"source": doc_name, "chunk": i}]
        )
    print(f"Ingested {len(chunks)} chunks from {doc_name}")
    return len(chunks)

def ingest_all_documents():
    os.makedirs(DOCS_PATH, exist_ok=True)
    total = 0
    for filename in os.listdir(DOCS_PATH):
        filepath = os.path.join(DOCS_PATH, filename)
        doc_name = filename.replace('.', '_')
        if filename.endswith('.pdf'):
            total += ingest_pdf(filepath, doc_name)
        elif filename.endswith('.txt') or filename.endswith('.md'):
            total += ingest_text_file(filepath, doc_name)
    print(f"Total chunks ingested: {total}")
    return total

def list_ingested_docs():
    try:
        results = collection.get()
        sources = list(set([m['source'] for m in results['metadatas']]))
        return sources
    except Exception:
        return []