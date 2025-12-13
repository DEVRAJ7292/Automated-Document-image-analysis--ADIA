# ADIA — Automated Document Intelligence

ADIA is an end-to-end **document intelligence system** that ingests PDFs and images, extracts text intelligently, and answers natural-language questions over the content using a Retrieval-Augmented Generation (RAG) pipeline.

This project is designed as a **production-style backend system**, not a tutorial or proof-of-concept.

---

## 🚀 What ADIA Does

- Upload PDFs and images
- Native PDF text extraction (OCR used only when necessary)
- OCR normalization for dates, numbers, and noisy text
- Semantic embeddings and vector search
- Natural-language question answering over documents
- Lightweight UI for demos and client interaction
- Fully containerized using Docker

---

## 🧠 High-Level Architecture

Upload Document ↓ Native PDF Extraction ↓ OCR (Fallback Only) ↓ Text Normalization ↓ Sentence Embeddings ↓ FAISS Vector Index ↓ Semantic Retrieval ↓ LLM (Gemini) ↓ Answer

---

## 🛠 Tech Stack

### Backend
- FastAPI
- Pydantic
- SQLite (query logging)

### AI / ML
- SentenceTransformers
- FAISS (vector search)
- Gemini API (LLM)

### Document Processing
- pdfplumber
- Tesseract OCR

### Frontend
- HTML
- Tailwind CSS

### Infrastructure
- Docker
- Docker Compose

---

## 🖥 Demo UI

The repository includes a lightweight UI intended for:
- Uploading documents
- Asking natural-language questions
- Viewing extracted answers

The UI is intentionally minimal to keep the focus on **backend intelligence and data flow**.

---

## 🐳 Running Locally with Docker

### Prerequisites
- Docker
- Docker Compose

### Run
```bash
docker compose build
docker compose up

Access

API Docs: http://localhost:8000/docs

UI: Open ui/ui.html in a browser



---

📂 Repository Structure

ADIA/
├── Dockerfile
├── docker-compose.yml
├── README.md
├── requirements.txt
├── src/
│   └── adia/
│       ├── api/
│       ├── core/
│       ├── embeddings/
│       ├── ocr/
│       ├── rag/
│       └── services/
└── ui/
    └── ui.html


---

🎯 Design Principles

Clear separation of concerns

Deterministic document processing

No hardcoded secrets

Persistent vector storage

Model lifecycle managed to avoid reload latency

Docker-first deployment mindset



---

📌 Project Status

Core backend: ✅ Complete

OCR + PDF extraction: ✅ Complete

Vector search + RAG: ✅ Complete

UI: ✅ Complete

Dockerization: ✅ Complete

Cloud deployment: 🔜 In progress



---

👤 Author

Devraj Gadhvi

Author: Devraj Gadhvi
