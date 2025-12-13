FROM python:3.11-slim

# System deps (OCR + PDF)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Working directory
WORKDIR /app

# Install python deps first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src/ src/
COPY data/ data/

# Environment
ENV PYTHONPATH=/app/src

# Expose API port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "adia.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
