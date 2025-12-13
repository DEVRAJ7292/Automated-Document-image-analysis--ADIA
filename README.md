# ADIA — Automated Document & Image Analysis

ADIA is an end-to-end document intelligence system that ingests PDFs/images, extracts text (native PDF first, OCR fallback), builds semantic embeddings, and answers questions using a RAG pipeline.

## What it does
- Upload PDFs / images
- Native PDF text extraction with OCR fallback
- Text normalization
- Semantic embeddings (SentenceTransformers)
- Vector search with FAISS
- Question answering via Gemini
- FastAPI backend
- Simple, clean UI
- Dockerized with persistent storage

## Tech Stack
- **Backend:** FastAPI, Pydantic
- **AI:** SentenceTransformers, FAISS, Gemini
- **OCR:** Tesseract
- **PDF:** pdfplumber
- **DB:** SQLite (query logs)
- **UI:** HTML + Tailwind
- **Infra:** Docker, Docker Compose

## Run with Docker
```bash
docker compose build
docker compose up
