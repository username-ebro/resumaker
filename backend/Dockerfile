# Use Python official image instead of Nixpacks
FROM python:3.12-slim

# Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    pango1.0-tools \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    libcairo2 \
    libgobject-2.0-0 \
    libglib2.0-0 \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose port (Railway will set PORT env var)
ENV PORT=8000

# Start command - use startup script
CMD ["/app/start.sh"]
