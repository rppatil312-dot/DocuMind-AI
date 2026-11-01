
import pymupdf

def extract_text_from_pdf(file_path: str):
    document = pymupdf.open(file_path)

    pages = []

    for page_number, page in enumerate(document):
        text = page.get_text("text")

        if text.strip():
            pages.append({
                "page": page_number + 1,
                "text": text
            })

    document.close()
    return pages
