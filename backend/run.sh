#!/bin/bash
# BIM Application Production Startup Script

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}BIM Application Startup${NC}"
echo -e "${BLUE}================================${NC}"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${GREEN}✓ Project root: ${PROJECT_ROOT}${NC}"

# Check if dist folder exists
if [ ! -d "$PROJECT_ROOT/dist" ]; then
    echo -e "${YELLOW}⚠ Frontend not built. Building now...${NC}"
    cd "$PROJECT_ROOT"
    npm run build
    echo -e "${GREEN}✓ Frontend built${NC}"
fi

# Set environment variables
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1

# Change to backend directory and start
cd "$SCRIPT_DIR"

echo -e "${GREEN}✓ Starting Backend API...${NC}"
echo -e "${BLUE}Access the application at: http://localhost:8000${NC}"
echo -e "${BLUE}API Docs at: http://localhost:8000/docs${NC}"
echo -e "${BLUE}================================${NC}\n"

python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
