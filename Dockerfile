# ============================================================
# UPLOADER-BOT-V4
# Railway Production Dockerfile
# ============================================================

FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive \
    DENO_INSTALL=/root/.deno \
    PATH=/root/.deno/bin:$PATH

# System dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        curl \
        ca-certificates \
        jq \
        unzip \
        tini \
        procps \
    && rm -rf /var/lib/apt/lists/*

# Install Deno
RUN curl -fsSL https://deno.land/install.sh | sh

RUN deno --version && \
    ffmpeg -version 2>&1 | head -1

# Application
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install --no-cache-dir -r requirements.txt

# Copy bot
COPY . .

# Runtime directory
RUN mkdir -p /app/DOWNLOADS

# Validate installation
RUN python -m pip check && \
    test -f /app/bot.py

# Proper signal handling
ENTRYPOINT ["/usr/bin/tini", "--"]

# Start bot
CMD ["python", "-u", "bot.py"]
