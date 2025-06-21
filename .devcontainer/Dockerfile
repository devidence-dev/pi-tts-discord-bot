FROM python:3.13.5-slim-bookworm

# Install system dependencies for TTS and audio processing
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    ffmpeg \
    espeak \
    espeak-data \
    libespeak1 \
    libespeak-dev \
    git \
    curl \
    rustc \
    cargo \
    && rm -rf /var/lib/apt/lists/*

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /workspace

# Set Python path
ENV PYTHONPATH=/workspace

# Run uv sync when container starts
COPY pyproject.toml uv.lock* ./
RUN uv sync
