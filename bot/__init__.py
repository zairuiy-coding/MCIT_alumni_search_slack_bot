
import logging

from flask import Flask
from slack_sdk import WebClient
from slackeventsapi import SlackEventAdapter

from bot.celery_utils import make_celery
from config import Config

def create_app():
    """
    Creates and configures the Flask application, sets up the Slack event adapter,
    initializes the Slack client, and configures Celery.
    
    Returns:
        tuple: A tuple containing the Flask app, Slack event adapter, Slack client, bot ID, and Celery instance.
    """
    app = Flask(__name__)

    # Set up logging
    setup_logging()
    
    # Load config
    app.config.from_object(Config)
    # Validate critical configs
    Config.validate_critical_configs()

    # Setup Slack components
    slack_event_adapter, slack_client, bot_id = setup_slack(app)

    # Store the slack client in extensions for later access
    app.extensions['slack_client'] = slack_client

    # Configure Celery
    celery = make_celery(app)

    return app, slack_event_adapter, slack_client, bot_id, celery

def setup_logging():
    """
    Configures the logging for the application.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_slack(app):
    """
    Configures the Slack event adapter and client.

    Returns:
        tuple: Slack event adapter, Slack client, and bot ID.
    """
    slack_event_adapter = SlackEventAdapter(Config.SIGNING_SECRET, '/slack/events', app)
    slack_client = WebClient(token=Config.SLACK_BOT_TOKEN)
    logging.info("Slack client and event adapter initialized")

    bot_id = slack_client.api_call("auth.test")['user_id']
    logging.info(f"Bot ID: {bot_id}")

    return slack_event_adapter, slack_client, bot_id

# Expose the celery instance at the module level
app, _, _, _, celery = create_app()
