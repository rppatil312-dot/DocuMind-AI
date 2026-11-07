
import chromadb
from pathlib import Path

# Create persistent ChromaDB storage
CHROMA_DIR = Path("chroma_db")
CHROMA_DIR.mkdir(exist_ok=True)

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

# Create or access the collection
collection = client.get_or_create_collection(
    name="documind_documents"
)


def store_embeddings(embedded_chunks: list, file_id: str):
    """
    Store PDF chunks and their embeddings in ChromaDB.
    """

    if not embedded_chunks:
        return 0

    collection.upsert(
        ids=[
            f"{file_id}_{chunk['chunk_id']}"
            for chunk in embedded_chunks
        ],
        embeddings=[
            chunk["embedding"]
            for chunk in embedded_chunks
        ],
        documents=[
            chunk["text"]
            for chunk in embedded_chunks
        ],
        metadatas=[
            {
                "file_id": file_id,
                "chunk_id": chunk["chunk_id"],
                "page": chunk["page"]
            }
            for chunk in embedded_chunks
        ]
    )

    return len(embedded_chunks)



def search_similar_chunks(
    query_embedding: list,
    file_id: str,
    n_results: int = 3
):
    """
    Search ChromaDB for the most relevant PDF chunks.
    """

    total_records = collection.count()

    if total_records == 0:
        return []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={"file_id": file_id}
    )

    retrieved_chunks = []

    if results["documents"] and results["documents"][0]:
        for i, document in enumerate(results["documents"][0]):
            retrieved_chunks.append({
                "text": document,
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })

    return retrieved_chunks

