#!/usr/bin/env python3
"""
BIM Application Runner
Starts the application with a single Python command
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    project_root = Path(__file__).parent
    backend_dir = project_root / "backend"
    
    # Check if frontend is built
    dist_dir = project_root / "dist"
    if not dist_dir.exists():
        print("📦 Frontend not built. Building now...")
        result = subprocess.run(["npm", "run", "build"], cwd=project_root)
        if result.returncode != 0:
            print("❌ Frontend build failed!")
            sys.exit(1)
        print("✅ Frontend built successfully!")
    
    # Add backend to Python path
    sys.path.insert(0, str(backend_dir))
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Set environment variables
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    os.environ["PYTHONUNBUFFERED"] = "1"
    
    # Run the backend
    print("🚀 Starting BIM Application...")
    print(f"📁 Project root: {project_root}")
    print(f"🔧 Backend directory: {backend_dir}")
    print("=" * 60)
    print(f"🌐 Access the application at: http://localhost:8000")
    print(f"📚 API Docs at: http://localhost:8000/docs")
    print("=" * 60)
    
    try:
        import uvicorn
        uvicorn.run(
            app="main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
