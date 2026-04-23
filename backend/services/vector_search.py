import os
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

VECTORDB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'vectordb')

openai_ef = OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-ada-002"
)

chroma_client = chromadb.PersistentClient(path=os.path.normpath(VECTORDB_PATH))

def search_relevant_docs(query: str, n_results: int = 3) -> str:
    try:
        collection = chroma_client.get_collection(
            name="documents",
            embedding_function=openai_ef
        )

        count = collection.count()
        if count == 0:
            return ""

        actual_n = min(n_results, count)

        results = collection.query(
            query_texts=[query],
            n_results=actual_n
        )

        if not results['documents'][0]:
            return ""

        chunks = results['documents'][0]
        sources = [m['source'] for m in results['metadatas'][0]]

        context = ""
        for chunk, source in zip(chunks, sources):
            context += f"\n[From {source}]:\n{chunk}\n"

        return context

    except Exception as e:
        print(f"Vector search error: {e}")
        return ""