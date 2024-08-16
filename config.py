import os

class Config:
    """
    Configuration class to store API keys and database connection strings.

    Attributes:
        OPENAI_API_KEY (str): API key for the OpenAI API.
        SLACK_BOT_TOKEN (str): Token for authenticating the Slack bot.
        DATABASE_URL (str): URL for connecting to the PostgreSQL database.
    """
    
    # open ai
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # backend database
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # slack config
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

    # Celery Configuration
    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    # Ensure critical environment variables are loaded
    if not SLACK_BOT_TOKEN:
        raise ValueError("SLACK_BOT_TOKEN environment variable is not set.")
    if not SIGNING_SECRET:
        raise ValueError("SLACK_SIGNING_SECRET environment variable is not set.")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set.")
    