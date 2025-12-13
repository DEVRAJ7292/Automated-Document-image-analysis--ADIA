FROM python:3.11-slim

# ─────────────────────────────
# System dependencies (OCR / PDF)
# ─────────────────────────────
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# ─────────────────────────────
# App setup
# ─────────────────────────────
WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ src/
COPY index.html .

# ✅ THIS IS THE CRITICAL LINE
ENV PYTHONPATH=/app/src

# Hugging Face uses port 7860
EXPOSE 7860

# ─────────────────────────────
# Start FastAPI
# ─────────────────────────────
CMD ["uvicorn", "adia.api.main:app", "--host", "0.0.0.0", "--port", "7860"]# ─────────────────────────────
# Start FastAPI
# ─────────────────────────────
CMD ["uvicorn", "adia.api.main:app", "--host", "0.0.0.0", "--port", "7860"]# -----------------------------
# Hugging Face required port
# -----------------------------
EXPOSE 7860

# -----------------------------
# Start FastAPI (HF-compatible)
# -----------------------------
CMD ["uvicorn", "adia.api.main:app", "--host", "0.0.0.0", "--port", "7860"]
