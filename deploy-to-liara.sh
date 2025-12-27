#!/bin/bash

# Deploy script for Liara
# Usage: ./deploy-to-liara.sh

set -e

echo "🚀 BIM Backend Deployment Script"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "backend/Dockerfile" ]; then
    echo "❌ Dockerfile not found in backend/"
    echo "Please run this script from the project root"
    exit 1
fi

echo "✅ Found backend/Dockerfile"

# Check Liara CLI
if ! command -v liara &> /dev/null; then
    echo "❌ Liara CLI not installed"
    echo "Install with: npm install -g @liara/cli"
    exit 1
fi

echo "✅ Liara CLI found"

# Navigate to backend
cd backend

echo ""
echo "📦 Starting deployment..."
echo "Directory: $(pwd)"

# Deploy
liara deploy --detach

echo ""
echo "✅ Deployment started!"
echo ""
echo "📋 Next steps:"
echo "1. Check deployment status: liara logs"
echo "2. Verify health: ./check-health.sh"
echo "3. Set environment variables in Liara Dashboard"
echo "4. Allocate disks (data and uploads)"
echo ""
echo "💡 For more info: cat ../LIARA_QUICK_START.md"
