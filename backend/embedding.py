
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(text_chunks: list):
    """
    Convert text chunks into numerical embeddings.
    """

    if not text_chunks:
        return []

    texts = [chunk["text"] for chunk in text_chunks]

    embeddings = model.encode(texts)

    results = []

    for chunk, embedding in zip(text_chunks, embeddings):
        results.append({
            "chunk_id": chunk["chunk_id"],
            "page": chunk["page"],
            "text": chunk["text"],
            "embedding": embedding.tolist()
        })

    return results



def generate_query_embedding(query: str):
    """
    Convert a user question into a numerical embedding.
    """

    if not query.strip():
        raise ValueError("Query cannot be empty")

    embedding = model.encode(query)

    return embedding.tolist()
