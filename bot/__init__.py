
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
        task_cls=FlaskTask,
        include=['bot.commands']    # Ensure the task module is included
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

    # Initialize session with Redis
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = Redis.from_url(Config.REDIS_URL)
    app.config['SESSION_PERMANENT'] = False
    # app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_KEY_PREFIX'] = 'slack_session:'
    # app.config['SESSION_COOKIE_NAME'] = 'slack_session_cookie'
    # app.config['SECRET_KEY'] = Config.SECRET_KEY
    Session(app)
    logging.info(f"Connected to Redis at {Config.REDIS_URL}")

    # slack setup
    slack_event_adapter = SlackEventAdapter(
        Config.SIGNING_SECRET, '/slack/events', app)
    
    slack_client = WebClient(token=Config.SLACK_BOT_TOKEN)

    logging.info("Slack client and event adapter initialized")

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