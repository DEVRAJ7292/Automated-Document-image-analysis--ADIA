FROM python:3.11-slim

# -----------------------------
# System dependencies (OCR + PDF)
# -----------------------------
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Working directory
# -----------------------------
WORKDIR /app

# -----------------------------
# Python dependencies
# -----------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Copy source code
# -----------------------------
COPY src/ src/
COPY data/ data/

# -----------------------------
# Environment
# -----------------------------
ENV PYTHONPATH=/app/src

# -----------------------------
# Hugging Face required port
# -----------------------------
EXPOSE 7860

# -----------------------------
# Start FastAPI (HF-compatible)
# -----------------------------
CMD ["uvicorn", "adia.api.main:app", "--host", "0.0.0.0", "--port", "7860"]
