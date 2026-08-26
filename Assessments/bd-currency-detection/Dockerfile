FROM python:3.11-slim

WORKDIR /app

# System libraries
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# CPU-only PyTorch
RUN pip install --no-cache-dir \
    torch torchvision \
    --index-url https://download.pytorch.org/whl/cpu

# Application dependencies
RUN pip install --no-cache-dir \
    fastapi \
    "uvicorn[standard]" \
    python-multipart \
    Pillow \
    opencv-python-headless

# Ultralytics WITHOUT installing opencv-python
RUN pip install --no-cache-dir --no-deps ultralytics

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]