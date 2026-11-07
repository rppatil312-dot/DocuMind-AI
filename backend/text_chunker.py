
def split_text_into_chunks(
    pages: list,
    chunk_size: int = 500,
    overlap: int = 100
):
    """
    Split PDF page text into smaller chunks.
    Each chunk retains its original page number.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size")

    chunks = []
    chunk_id = 1

    for page in pages:
        text = " ".join(page["text"].split())
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            chunks.append({
                "chunk_id": chunk_id,
                "page": page["page"],
                "text": chunk_text
            })

            chunk_id += 1
            start += chunk_size - overlap

    return chunks
