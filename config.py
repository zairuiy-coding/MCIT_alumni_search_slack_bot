import os

class Config:
    """
    Configuration class for the application, responsible for loading and validating
    essential environment variables such as API keys, database URLs, and service configurations.

    Attributes:
        OPENAI_API_KEY (str): The API key for accessing the OpenAI API, used for processing user queries.
        SLACK_BOT_TOKEN (str): The authentication token for the Slack bot, enabling it to interact with Slack.
        SIGNING_SECRET (str): The signing secret for verifying requests from Slack.
        DATABASE_URL (str): The URL for connecting to the PostgreSQL database, storing application data.
        REDIS_URL (str): The URL for connecting to the Redis instance, used for session management and caching.
        REDIS_EXPIRATION_TIME (int): The expiration time (in seconds) for Redis keys, defaulting to 1 hour.
        CELERY_BROKER_URL (str): The URL for the message broker used by Celery, typically Redis in this setup.
        CELERY_RESULT_BACKEND (str): The backend used by Celery to store task results, typically Redis.

    Methods:
        validate_critical_configs():
            Validates the presence of critical environment variables required for the application to run.
            Raises a ValueError if any critical configuration is missing.
    """
    
    # open ai
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # backend database
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # slack config
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

    # Redis
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    REDIS_EXPIRATION_TIME = int(os.getenv('REDIS_EXPIRATION_TIME', 3600))  # Default to 1 hour if not set

    # Celery Configuration
    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    @classmethod
    def validate_critical_configs(cls):
        """
        Ensure that critical environment variables are loaded.

        Raises:
            ValueError: If any critical configuration is not set.
        """
        if not cls.SLACK_BOT_TOKEN:
            raise ValueError("SLACK_BOT_TOKEN environment variable is not set.")
        if not cls.SIGNING_SECRET:
            raise ValueError("SLACK_SIGNING_SECRET environment variable is not set.")
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is not set.")
