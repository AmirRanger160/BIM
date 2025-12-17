FROM node:18 AS frontend-builder

WORKDIR /frontend

# Copy package files
COPY package*.json ./
COPY vite.config.js ./
COPY index.html ./

# Copy source files
COPY src ./src
COPY public ./public

# Install dependencies and build
RUN npm ci --silent && npm run build


FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

# Install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# Copy backend application
COPY backend /app

# Create uploads directory
RUN mkdir -p /app/uploads

# Copy built frontend files from builder
COPY --from=frontend-builder /frontend/dist /app/dist

EXPOSE 8000

# Run the backend server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
