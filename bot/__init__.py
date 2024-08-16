
import logging
from celery import Celery, Task
from flask import Flask
from slack_sdk import WebClient
from slackeventsapi import SlackEventAdapter

from redis import Redis
from flask_session import Session

from config import Config

def make_celery(app):
    """
    Initialize and configure Celery within the Flask app context.
    """
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        task_cls=FlaskTask
    )
    celery_app.set_default()
    app.extensions['celery'] = celery_app
    return celery_app

def create_app():
    """
    Creates and configures the Flask application, sets up the Slack event adapter,
    initializes the Slack client, and configures Celery.
    
    Returns:
        tuple: A tuple containing the Flask app, Slack event adapter, Slack client, bot ID, and Celery instance.
    """
    app = Flask(__name__)

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Load config
    app.config.from_object(Config)

    # Initialize session
    Session(app)

    # slack setup
    slack_event_adapter = SlackEventAdapter(
        Config.SIGNING_SECRET, '/slack/events', app)

    slack_client = WebClient(token=Config.SLACK_BOT_TOKEN)

    # get the id of our bot
    bot_id = slack_client.api_call("auth.test")['user_id']

    # Log the bot ID
    logging.info(f"Bot ID: {bot_id}")

    # Store the slack client in extensions for later access
    app.extensions['slack_client'] = slack_client

    # Configure Celery
    celery = make_celery(app)

    return app, slack_event_adapter, slack_client, bot_id, celery

# Expose the celery instance at the module level
celery = make_celery(create_app()[0])