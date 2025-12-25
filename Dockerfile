# Build frontend
FROM node:18-alpine as frontend-build

WORKDIR /app

# Set API URL for production build
ENV VITE_API_URL=/api

# Copy frontend files
COPY package*.json ./
COPY src ./src
COPY public ./public
COPY index.html ./
COPY vite.config.js ./
COPY vite-plugin-spa-fallback.js ./

# Install dependencies and build
RUN npm install
RUN npm run build

# Python backend
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ .

# Copy built frontend to static directory
COPY --from=frontend-build /app/dist ./static

# Create uploads directory
RUN mkdir -p uploads/team uploads/certificates uploads/licenses

# Environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
