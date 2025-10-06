# syntax=docker/dockerfile:1

FROM python:3.10-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    net-tools \
  && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code
COPY . /app

# Create non-root user and set the correct permissions for the app
RUN useradd -ms /bin/bash appuser \
  && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Ensure the entrypoint.sh script has executable permissions
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Set the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
