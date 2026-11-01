# 📚 DocuMind AI

### Intelligent PDF Question Answering System using AI

DocuMind AI is an AI-powered project designed to make reading and understanding PDF documents easier. It aims to allow users to upload PDF files and ask questions about their content using Retrieval-Augmented Generation (RAG).

## 🎯 Project Overview

Finding specific information in large PDF documents can be time-consuming. DocuMind AI aims to simplify this process by extracting document content and providing relevant answers to user questions.

## ✨ Features

### Implemented
- PDF upload using FastAPI.
- PDF file validation.
- Text extraction using PyMuPDF.
- Page-wise text extraction.
- Backend health-check API.

### Planned
- Text chunking.
- Embeddings using Sentence Transformers.
- Vector database using ChromaDB.
- Semantic search.
- AI-generated answers.
- React frontend.

## 🛠️ Technologies Used

- Python
- FastAPI
- Uvicorn
- PyMuPDF
- Sentence Transformers
- ChromaDB
- OpenAI API
- React.js (planned)

## 📂 Project Structure

```text
DocuMind-AI/
├── backend/
│   ├── main.py
│   ├── document_processor.py
│   └── uploads/
├── .gitignore
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/rppatil312-dot/DocuMind-AI.git
```

### 2. Open the backend folder

```bash
cd DocuMind-AI/backend
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

```powershell
.\venv\Scripts\Activate
```

### 5. Install dependencies

```bash
pip install fastapi uvicorn python-multipart pymupdf sentence-transformers chromadb openai python-dotenv
```

### 6. Start the server

```bash
uvicorn main:app --reload
```

Backend URL: http://127.0.0.1:8000

API Documentation: http://127.0.0.1:8000/docs

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/upload` | Upload and extract PDF text |

## 🧠 Planned RAG Workflow

1. Upload PDF.
2. Extract text.
3. Split text into chunks.
4. Generate embeddings.
5. Store embeddings in ChromaDB.
6. Retrieve relevant information.
7. Generate answers using an AI model.

## 🚀 Future Improvements

- Multiple PDF support.
- Chat history.
- OCR for scanned documents.
- User authentication.
- Docker deployment.

## 👩‍💻 Developer

**Rutuja Patil**

GitHub: [rppatil312-dot](https://github.com/rppatil312-dot)

---

⭐ If you like this project, consider giving it a star!

*DocuMind AI – Making document understanding smarter and easier.*