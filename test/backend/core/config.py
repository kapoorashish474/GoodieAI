import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = "postgresql://ashishkapoor@localhost:5432/hn_analytics"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Hacker News API
    HN_API_BASE_URL: str = "https://hacker-news.firebaseio.com/v0"
    HN_TOP_STORIES_LIMIT: int = 50
    
    # Application
    APP_NAME: str = "Hacker News Analytics Dashboard"
    DEBUG: bool = False
    
    # AI Keywords for detection
    AI_KEYWORDS: list[str] = [
        "ChatGPT", "Claude", "Gemini", "OpenAI", "Anthropic", "Google AI",
        "GPT-4", "GPT-3", "LLM", "Large Language Model", "AI", "Artificial Intelligence",
        "Machine Learning", "ML", "Deep Learning", "Neural Network", "Transformer",
        "Bard", "Copilot", "GitHub Copilot", "DALL-E", "Midjourney", "Stable Diffusion"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings() 