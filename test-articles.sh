#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🧪 تست سیستم مقالات GeoBiro${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check backend server
echo -e "${YELLOW}1️⃣  بررسی سرور بکند...${NC}"
if curl -s http://localhost:8000/api/articles > /dev/null 2>&1; then
    echo -e "${GREEN}✓ سرور بکند اجرا می‌شود${NC}"
else
    echo -e "${RED}✗ سرور بکند اجرا نمی‌شود!${NC}"
    echo -e "${YELLOW}لطفا ابتدا بکند را شروع کنید:${NC}"
    echo -e "${BLUE}  cd backend && python3 main.py${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}2️⃣  بررسی مقالات موجود...${NC}"
COUNT=$(curl -s http://localhost:8000/api/articles | jq 'length')
echo -e "${BLUE}تعداد مقالات: ${GREEN}$COUNT${NC}"

if [ "$COUNT" -eq 0 ]; then
    echo -e "${YELLOW}هیچ مقاله‌ای یافت نشد. Seed می‌کنیم...${NC}"
    RESULT=$(curl -s -X POST http://localhost:8000/api/articles/seed-demo)
    echo -e "${GREEN}✓ نتیجه:${NC}"
    echo "$RESULT" | jq .
else
    echo -e "${GREEN}✓ مقالات قبلاً موجود هستند${NC}"
fi

echo ""
echo -e "${YELLOW}3️⃣  بررسی API endpoints...${NC}"

# Check articles endpoint
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/articles)
echo "  GET /api/articles: $([ $RESPONSE -eq 200 ] && echo -e "${GREEN}$RESPONSE ✓${NC}" || echo -e "${RED}$RESPONSE ✗${NC}")"

# Check first article
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/articles/1)
echo "  GET /api/articles/1: $([ $RESPONSE -eq 200 ] && echo -e "${GREEN}$RESPONSE ✓${NC}" || echo -e "${RED}$RESPONSE ✗${NC}")"

# Check tags endpoint
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/articles/tags/all)
echo "  GET /api/articles/tags/all: $([ $RESPONSE -eq 200 ] && echo -e "${GREEN}$RESPONSE ✓${NC}" || echo -e "${RED}$RESPONSE ✗${NC}")"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ تمام تست‌ها انجام شدند!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}صفحات قابل دسترس:${NC}"
echo "  • صفحه اصلی: ${BLUE}http://localhost:5173${NC}"
echo "  • آرشیو مقالات: ${BLUE}http://localhost:5173/#/articles${NC}"
echo "  • Admin: ${BLUE}http://localhost:5173/#/admin-login${NC}"
echo ""
