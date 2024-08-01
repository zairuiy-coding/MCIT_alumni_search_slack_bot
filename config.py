import os

class Config:
    """
    Configuration class to store API keys and database connection strings.

    Attributes:
        SLACK_BOT_TOKEN (str): Token for authenticating the Slack bot.
        DATABASE_URL (str): URL for connecting to the PostgreSQL database.
    """
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")