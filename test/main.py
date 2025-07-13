#!/usr/bin/env python3
"""
Main entry point for the Hacker News Analytics Dashboard Backend.
"""

import sys
import argparse
import uvicorn
from backend.api import app
from backend.workers.background_processor import BackgroundProcessor
from backend.database.database import engine
from backend.database.models import Base


def create_tables():
    """Create database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def run_api_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Run the FastAPI server."""
    print(f"Starting API server on {host}:{port}")
    uvicorn.run(app, host=host, port=port, reload=reload)


def run_background_processor():
    """Run the background processor."""
    print("Starting background processor...")
    processor = BackgroundProcessor()
    processor.run()


def run_celery_worker():
    """Run the Celery worker."""
    print("Starting Celery worker...")
    from backend.core.celery_app import celery_app
    celery_app.worker_main(['worker', '--loglevel=info'])


def run_celery_beat():
    """Run the Celery beat scheduler."""
    print("Starting Celery beat scheduler...")
    from backend.core.celery_app import celery_app
    celery_app.worker_main(['beat', '--loglevel=info'])


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Hacker News Analytics Dashboard Backend")
    parser.add_argument(
        "command",
        choices=["api", "processor", "create-tables", "celery-worker", "celery-beat"],
        help="Command to run"
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host for API server")
    parser.add_argument("--port", type=int, default=8000, help="Port for API server")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for API server")
    
    args = parser.parse_args()
    
    if args.command == "api":
        run_api_server(args.host, args.port, args.reload)
    elif args.command == "processor":
        run_background_processor()
    elif args.command == "create-tables":
        create_tables()
    elif args.command == "celery-worker":
        run_celery_worker()
    elif args.command == "celery-beat":
        run_celery_beat()
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    main() 