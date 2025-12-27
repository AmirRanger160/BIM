#!/bin/bash

# Entrypoint script for FastAPI backend
# Handles database initialization and user creation

set -e

echo "🚀 Initializing FastAPI Backend..."

# Create necessary directories
mkdir -p /app/data /app/uploads/team /app/uploads/certificates /app/uploads/licenses

echo "📁 Directories created"

# Initialize database and create admin user
echo "🔧 Initializing database..."
python /app/init_admin.py

echo "✅ Database initialized"

# Start the application
echo "🌐 Starting FastAPI application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
