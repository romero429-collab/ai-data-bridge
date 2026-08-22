# Multi-stage production container for AI-to-AI Data Bridge (DDS-Bridge)
# Pre-packaged with Chromium and Playwright rendering dependencies
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Ensure Chromium headless browser binary is ready with universal permissions
RUN playwright install chromium && \
    chmod -R 777 /ms-playwright

# Copy application source
COPY . .
RUN chmod -R 777 /app

# Expose target network port (8080 / 7860)
EXPOSE 8080
EXPOSE 7860

# Launch production ASGI server
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080}"]
