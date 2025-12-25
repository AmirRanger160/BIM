# Frontend-Backend Integration Plan: Serving Vue.js SPA from FastAPI

## Overview

This plan outlines the steps to integrate the built Vue.js frontend (dist files) into the FastAPI backend service. The integration will serve static files directly from FastAPI, handle SPA routing fallbacks, and ensure proper API routing separation.

## Current Project Structure Analysis

### Frontend (Vue.js + Vite)
- Build configuration: `vite.config.js` outputs to `dist/` directory with `assets/` subdirectory
- Build command: `npm run build`
- Custom SPA fallback plugin: `vite-plugin-spa-fallback.js` (used in development)
- API client: `src/services/api.js` already configured for backend integration

### Backend (FastAPI)
- Main application: `backend/main.py`
- Static file mounting: Already mounts `/uploads` for uploads directory
- Static directory check: Looks for `backend/static/` and mounts `/assets` and `/` if exists
- API routes: All prefixed with `/api` (auth, services, projects, etc.)
- CORS configured for frontend URLs

## Step-by-Step Integration Plan

### Phase 1: Frontend Build Preparation

1. **Environment Configuration**
   - Ensure `.env` or environment variables set `VITE_API_URL` pointing to production API endpoint
   - For local development: `http://localhost:8000/api`
   - For production: `https://api.geobiro.ba/api` or relative `/api`

2. **Build Frontend**
   ```bash
   npm install
   npm run build
   ```
   - This creates `dist/` directory with `index.html` and `assets/` folder

### Phase 2: Static File Integration

3. **Prepare Backend Static Directory**
   - Create `backend/static/` directory if not exists
   - Copy contents of `dist/` to `backend/static/`
   - Ensure `backend/static/index.html` and `backend/static/assets/` exist

4. **Update Backend Configuration (main.py)**
   - Modify static file mounting to properly handle SPA routing
   - Current code mounts `/assets` and `/` to static directory
   - Need to add SPA fallback for client-side routing

### Phase 3: Backend Modifications

5. **Implement SPA Fallback Routing**
   - Remove or modify the current static mounting that serves `/` directly
   - Mount only `/assets` to `static/assets`
   - Add catch-all route `/{path:path}` that serves `static/index.html` for non-API paths
   - Ensure API routes (`/api/*`), uploads (`/uploads/*`), and assets (`/assets/*`) are excluded from fallback

6. **Update Dependencies**
   - No new dependencies required; FastAPI's `FileResponse` can serve static files

### Phase 4: Testing and Validation

7. **Local Integration Testing**
   - Start FastAPI backend: `cd backend && uvicorn main:app --reload`
   - Access `http://localhost:8000` (should serve the Vue app)
   - Test client-side routing (e.g., `/about`, `/projects`) - should load index.html and handle routing in Vue
   - Verify API calls work (`/api/*` routes)
   - Test file uploads (`/uploads/*`)

8. **CORS and Security Validation**
   - Ensure CORS allows frontend domain in production
   - Verify static files are served with appropriate headers
   - Check that API endpoints remain secure

### Phase 5: Deployment Considerations

9. **Docker Integration**
   - Update `Dockerfile` and `docker-compose.yml` to include frontend build step
   - Option 1: Multi-stage build - build frontend in Docker, copy to backend image
   - Option 2: Build frontend separately, copy dist files to backend context
   - Ensure static files are included in backend container

10. **Production Environment Setup**
    - Set `FRONTEND_URL` in backend environment for CORS
    - Configure reverse proxy (nginx) if needed for static file serving optimization
    - Enable gzip compression for static assets
    - Set appropriate cache headers for assets (long cache) vs index.html (no-cache)

## Potential Challenges and Solutions

### SPA Routing Issues
- **Challenge**: Direct URL access to routes like `/about` returns 404
- **Solution**: Implement catch-all route that serves index.html for unmatched paths
- **Code Example**:
  ```python
  from fastapi.responses import FileResponse
  import os

  static_dir = os.path.join(os.path.dirname(__file__), "static")

  @app.get("/{path:path}")
  async def serve_spa(path: str):
      # Skip API, uploads, and assets paths
      if path.startswith(("api/", "uploads/", "assets/")):
          raise HTTPException(status_code=404, detail="Not found")
      # Serve index.html for SPA routes
      index_path = os.path.join(static_dir, "index.html")
      if os.path.exists(index_path):
          return FileResponse(index_path)
      raise HTTPException(status_code=404, detail="Not found")
  ```

### Static File Conflicts
- **Challenge**: API routes conflict with static file paths
- **Solution**: Ensure API routes are properly prefixed and static mounting excludes API paths

### Build Process Integration
- **Challenge**: Coordinating frontend and backend builds in deployment
- **Solution**: Use Docker multi-stage builds or CI/CD pipeline that builds frontend first

### Cache Invalidation
- **Challenge**: Browser caching of old assets after deployment
- **Solution**: Use Vite's asset hashing (automatic) and set cache headers appropriately

## Best Practices

- **Security**: Ensure static files don't expose sensitive information
- **Performance**: Enable compression and caching for static assets
- **Monitoring**: Add logging for static file requests if needed
- **Versioning**: Consider API versioning for future compatibility
- **Testing**: Include integration tests that verify static file serving and API connectivity

## Expected File Changes

1. `backend/main.py`: Add SPA fallback route, adjust static mounting
2. `backend/static/`: New directory with built frontend files
3. `Dockerfile`: Update to include frontend build step
4. `docker-compose.yml`: Ensure proper volume mounting if needed

## Next Steps

After review and approval of this plan:
1. Implement the backend modifications
2. Build and integrate frontend
3. Test thoroughly in development
4. Deploy to staging environment
5. Validate production deployment

This plan ensures a seamless integration where the FastAPI backend serves both the API and the Vue.js SPA, maintaining proper separation and SPA functionality.