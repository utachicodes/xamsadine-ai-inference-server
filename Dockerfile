# Dockerfile
FROM nvidia/cuda:12.4.0-runtime-ubuntu22.04

ENV PYTHON_VERSION=3.11
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python${PYTHON_VERSION} \
    python3-pip \
    python3-dev \
    git \
    build-essential \
    ffmpeg \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
COPY app.py .

# Install Python packages
RUN pip3 install --no-cache-dir --timeout=300 torch torchaudio
RUN pip3 install --no-cache-dir -r requirements.txt

ENV AIP_HTTP_PORT=8080
ENV AIP_HEALTH_ROUTE=/health
ENV AIP_PREDICT_ROUTE=/predict
ENV HF_TOKEN=""

EXPOSE 8080
CMD ["python3", "app.py"]