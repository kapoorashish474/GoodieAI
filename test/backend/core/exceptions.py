"""
Custom exceptions for the application.
"""

from fastapi import HTTPException, status


class DatabaseConnectionError(HTTPException):
    """Raised when database connection fails."""
    def __init__(self, detail: str = "Database connection failed"):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)


class RedisConnectionError(HTTPException):
    """Raised when Redis connection fails."""
    def __init__(self, detail: str = "Redis connection failed"):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)


class HackerNewsAPIError(HTTPException):
    """Raised when Hacker News API fails."""
    def __init__(self, detail: str = "Hacker News API error"):
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)


class StoryNotFoundError(HTTPException):
    """Raised when a story is not found."""
    def __init__(self, story_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Story with ID {story_id} not found"
        )


class TaskNotFoundError(HTTPException):
    """Raised when a task is not found."""
    def __init__(self, task_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task with ID {task_id} not found"
        )


class ValidationError(HTTPException):
    """Raised when data validation fails."""
    def __init__(self, detail: str = "Validation error"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail) 