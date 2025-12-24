#!/bin/bash

# GeoBiro Backend Setup Script
# This script sets up the FastAPI backend environment

set -e

echo "🚀 GeoBiro FastAPI Backend Setup"
echo "=================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 --version

# Create virtual environment (optional but recommended)
if [ ! -d "venv" ]; then
    echo "✓ Creating Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created and activated"
else
    echo "✓ Virtual environment already exists"
    source venv/bin/activate
fi

# Install dependencies
echo ""
echo "✓ Installing Python dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "✓ Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your configuration"
    echo "   - Database URL"
    echo "   - Redis URL"
    echo "   - Secret Key"
    echo "   - Email SMTP settings"
else
    echo "✓ .env file already exists"
fi

# Create uploads directory
echo ""
echo "✓ Creating uploads directory..."
mkdir -p uploads/team
mkdir -p uploads/certificates
mkdir -p uploads/licenses

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure your .env file with database and email settings"
echo "2. Ensure PostgreSQL and Redis are running"
echo "3. Run: uvicorn main:app --reload"
echo ""
echo "API will be available at: http://localhost:8000"
echo "API docs at: http://localhost:8000/api/docs"
