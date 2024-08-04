import os

class Config:
    """
    Configuration class to store API keys and database connection strings.

    Attributes:
        OPENAI_API_KEY (str): API key for the OpenAI API.
        SLACK_BOT_TOKEN (str): Token for authenticating the Slack bot.
        DATABASE_URL (str): URL for connecting to the PostgreSQL database.
    """
    # Read the OPENAI_API_KEY key
    with open('openai.txt', 'r') as file:
        OPENAI_API_KEY = file.readline().strip() # Read the key and remove any trailing spaces or newlines

    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")