# Troubleshooting: 405 Method Not Allowed Error

## Problem
You're getting a **405 (Method Not Allowed)** error when trying to POST to `/api/comments`:

```
POST https://...8000.app.github.dev/api/comments 405 (Method Not Allowed)
```

## Root Causes & Solutions

### Solution 1: Rebuild and Restart Backend ✓

The most common cause is stale code or an issue with route registration:

```bash
# 1. Stop the backend (Ctrl+C)

# 2. Rebuild the frontend
npm run build

# 3. Restart the backend
cd backend
python main.py

# 4. Clear browser cache and reload
# Ctrl+Shift+Delete (Windows/Linux) or Cmd+Shift+Delete (Mac)
# Or open DevTools (F12) → Application → Clear all
```

### Solution 2: Verify API Routes are Registered

Check that the POST endpoint exists:

```bash
cd backend

python3 << 'EOF'
from main import app
from fastapi.routing import APIRoute

# List all comment routes
print("Comment Routes:")
for route in app.routes:
    if isinstance(route, APIRoute) and 'comments' in route.path:
        methods = ",".join(route.methods) if hasattr(route, 'methods') else 'ALL'
        print(f"  {methods:30} {route.path}")
EOF
```

Should show:
```
Comment Routes:
  GET                            /api/comments/stats/summary
  GET                            /api/comments/
  GET                            /api/comments/{comment_id}
  POST                           /api/comments/
  PUT                            /api/comments/{comment_id}
  PUT                            /api/comments/{comment_id}/approve
  DELETE                         /api/comments/{comment_id}
```

### Solution 3: Check Request URL

Make sure the frontend is sending requests to the correct URL:

**In Browser DevTools:**
1. Open: F12 → Network Tab
2. Try to submit a comment
3. Look for the POST request to `/api/comments`
4. Check the request headers and URL

The URL should be:
- `http://localhost:8000/api/comments` (local)
- `https://<codespace>.app.github.dev/api/comments` (Codespaces)

### Solution 4: Verify Backend Configuration

Ensure the API routes are properly registered in `main.py`:

```python
# These lines should exist in main.py around line 105-112:
app.include_router(auth_routes.router)
app.include_router(articles.router)
app.include_router(gallery.router)
app.include_router(other.router)
app.include_router(upload.router)
app.include_router(admin.router)
app.include_router(comments.router)  # ← Comments router must be included
```

### Solution 5: Check Comments Router Exists

Verify the comments router is properly defined:

```bash
cd backend
python3 << 'EOF'
from app.routes import comments
print(f"Comments router prefix: {comments.router.prefix}")
print(f"Comments router routes: {len(comments.router.routes)}")
EOF
```

Should show:
```
Comments router prefix: /api/comments
Comments router routes: 7
```

### Solution 6: Fix Trailing Slash Issues

Sometimes FastAPI is strict about trailing slashes. If you see POST to `/api/comments/` (with slash) working but `/api/comments` (without slash) failing:

Update `src/api/services.js`:

```javascript
// Add trailing slash to endpoints
export const createComment = async (commentData) => {
  const response = await apiClient.post('/api/comments/', commentData)  // Add /
  return response.data
}
```

Or configure FastAPI to handle trailing slashes automatically in `backend/main.py`:

```python
from fastapi import FastAPI
from fastapi.routing import Mount

app = FastAPI()

# This allows both /api/comments and /api/comments/ to work
app.router.redirect_slashes = True
```

## Debug Checklist

- [ ] Backend is running without errors
- [ ] Frontend is built: `npm run build` succeeded
- [ ] Browser cache is cleared (F12 → Clear all)
- [ ] Comments router shows in route list
- [ ] POST route exists in `/api/comments/`
- [ ] No SyntaxWarning in backend output
- [ ] CORS headers allow POST method

## Check Backend Logs

When starting the backend, you should see:

```
✅ Frontend assets mounted from /path/to/dist/assets
✅ Database initialized
✅ Admin user exists: admin@bim.com
✅ Sample data already exists
✓ Server running on 0.0.0.0:8000
```

If you see errors, fix them before continuing.

## Network Tab Details

Check what the browser is actually sending:

1. Open DevTools: F12
2. Go to Network tab
3. Try to submit a comment
4. Click on the POST request to `/api/comments`
5. Check:
   - **Headers** → Request Method should be POST
   - **Headers** → Content-Type should be `application/json`
   - **Payload** → Should have name, email, content, rating, etc.
   - **Response** → Should show error details if it fails

## Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| 405 Method Not Allowed | POST endpoint not registered | Restart backend after build |
| 404 Not Found | Route doesn't exist | Check router is included |
| 403 Forbidden | Missing auth token | Login first (Admin panel) |
| CORS error | Different origin | Backend and frontend on same server |
| 500 Internal Server | Database error | Check server logs |

## Quick Test

Test the API endpoint manually:

```bash
# Using curl
curl -X POST http://localhost:8000/api/comments \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "content": "This is a test comment with enough characters",
    "rating": 5,
    "content_type": "article",
    "content_id": 1
  }'
```

Should return:
- Success: 201 status code with comment data
- Error: 400/422 with validation error message
- NOT 405 Method Not Allowed

## Still Having Issues?

1. **Stop backend**: Ctrl+C
2. **Rebuild everything**:
   ```bash
   npm run build
   cd backend && python main.py
   ```
3. **Check all logs** in terminal output
4. **Verify routes** using the debug script above
5. **Test manually** using curl command

If it still doesn't work:
- Check that `/api/comments POST` route exists
- Verify `app.include_router(comments.router)` is in main.py
- Ensure `backend/app/routes/comments.py` has `@router.post("/", ...)` endpoint
- Review browser Network tab for exact error

---

**The 405 error should be resolved after rebuilding and restarting!**
