#!/bin/bash

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}GeoBiro - مقالات را Seed کنید${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if server is running
echo -e "${YELLOW}💡 بررسی سرور...${NC}"
if ! nc -z localhost 8000 2>/dev/null; then
    echo -e "${YELLOW}⚠️  سرور در پورت 8000 شنیدار نیست${NC}"
    echo -e "${YELLOW}لطفا ابتدا بکند را اجرا کنید:${NC}"
    echo -e "${BLUE}cd backend && python3 main.py${NC}"
    exit 1
fi

echo -e "${GREEN}✓ سرور اجرا می‌شود${NC}"
echo ""

# Seed articles
echo -e "${YELLOW}📝 مقالات نمونه را اضافه می‌کنیم...${NC}"
RESPONSE=$(curl -s -X POST http://localhost:8000/api/articles/seed-demo)

echo -e "${GREEN}✓ پاسخ:${NC}"
echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ تمام! حالا می‌توانید مقالات را ببینید${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}صفحات قابل دسترس:${NC}"
echo "  • صفحه اصلی: http://localhost:5173 (مقالات برجسته)"
echo "  • آرشیو مقالات: http://localhost:5173/#/articles"
echo "  • Admin Panel: http://localhost:5173/#/admin-login"
echo ""
