# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (important for many Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better for layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose FastAPI default port
EXPOSE 8080

# Environment variable for FastAPI host/port
ENV PORT=8080

# Run Alembic migrations automatically on startup (optional but recommended)
# Then start FastAPI server using uvicorn
CMD alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port $PORT