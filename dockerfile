FROM python:3.11-slim

# System dependencies (OCR + PDF)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ src/
COPY data/ data/

# Expose port (Render requirement)
EXPOSE 8000

#  THIS IS THE MOST IMPORTANT PART
CMD ["uvicorn", "adia.main:app", "--host", "0.0.0.0", "--port", "8000"]
