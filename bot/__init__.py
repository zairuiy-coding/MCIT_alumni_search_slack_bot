
import logging
from flask import Flask
from slack_sdk import WebClient
from slackeventsapi import SlackEventAdapter

from config import Config

def create_app():
    """
    Creates and configures the Flask application, sets up the Slack event adapter, and initializes 
    the Slack client.

    Returns:
        tuple: A tuple containing the Flask app, Slack event adapter, Slack client, and bot ID.
    """
    app = Flask(__name__)

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    slack_event_adapter = SlackEventAdapter(
        Config.SIGNING_SECRET, '/slack/events', app)

    slack_client = WebClient(token=Config.SLACK_BOT_TOKEN)

    # get the id of our bot
    bot_id = slack_client.api_call("auth.test")['user_id']

    # Log the bot ID
    logging.info(f"Bot ID: {bot_id}")

    return app, slack_event_adapter, slack_client, bot_id
