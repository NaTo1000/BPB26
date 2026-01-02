#!/usr/bin/env python3
"""
Quick start script for running the Pinnacle Building Compliance Platform API server
"""

import uvicorn
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from bpb26.integrations.api import app


def main():
    """Start the API server"""
    print("=" * 70)
    print("Starting Pinnacle Building Compliance Platform API Server")
    print("=" * 70)
    print("\nAPI Documentation available at:")
    print("  - Swagger UI: http://localhost:8000/docs")
    print("  - ReDoc: http://localhost:8000/redoc")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70 + "\n")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()
