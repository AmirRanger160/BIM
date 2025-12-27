#!/bin/bash

# Health Check Debug Script for Liara

echo "🔍 Health Check Debug Script"
echo "=============================="

# Check if Liara CLI is installed
if ! command -v liara &> /dev/null; then
    echo "❌ Liara CLI not found"
    echo "Install with: npm install -g @liara/cli"
    exit 1
fi

echo "✅ Liara CLI found"

# Get app info
echo ""
echo "📊 Fetching app information..."
APP_INFO=$(liara get-app-info 2>/dev/null)

if [ $? -ne 0 ]; then
    echo "❌ Failed to get app info"
    echo "Make sure you're in the backend directory and logged in"
    exit 1
fi

echo "✅ App info retrieved"

# Extract URL
APP_URL=$(echo "$APP_INFO" | grep -oP '(?<=URL: ).*' | head -1)

if [ -z "$APP_URL" ]; then
    echo "❌ Could not find app URL"
    echo "Raw info:"
    echo "$APP_INFO"
    exit 1
fi

echo ""
echo "🌐 App URL: $APP_URL"

# Test health endpoint
echo ""
echo "🏥 Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "$APP_URL/health")
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | tail -1)
BODY=$(echo "$HEALTH_RESPONSE" | head -1)

echo "HTTP Status: $HTTP_CODE"
echo "Response: $BODY"

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Health check PASSED"
    exit 0
else
    echo "❌ Health check FAILED"
    echo ""
    echo "📋 Checking logs..."
    liara logs --tail 20
    exit 1
fi
