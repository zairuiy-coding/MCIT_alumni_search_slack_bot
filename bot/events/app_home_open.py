import logging
import redis
from bot import create_app
from config import Config

app, slack_event_adapter, slack_client, bot_id, celery = create_app()

# Initialize Redis client
redis_client = redis.StrictRedis.from_url(Config.REDIS_URL)

def handle_app_home_opened_event(event_data):
    """
    Handles the event when the bot is added to the workspace.
    Sends a welcome message to the user who added the bot.
    """
    event = event_data.get('event', {})
    user_id = event.get('user')

    session_key = f'welcomed_{user_id}'

    # Check if the user has been welcomed
    if not bool(redis_client.get(session_key)):
        # Send welcome message
        welcome_message = "Welcome to the MCIT Alumni Search Bot!\nPlease use the `/search-alumni` command followed by your query to find relevant alumni information."

        # User Manual Image URL
        image_url = "https://github.com/zairuiy-coding/MCIT_alumni_search_slack_bot/raw/main/user_manual.png"

        # Send message with image
        slack_client.chat_postMessage(
            channel=user_id,
            text=welcome_message,
            attachments=[
                {
                    "fallback": "User Manual",
                    "image_url": image_url,
                    "alt_text": "User Manual"
                }
            ]
        )

        # Set the key in Redis to mark that the user has been welcomed
        redis_client.set(session_key, "True", ex=Config.REDIS_EXPIRATION_TIME)
        logging.info(f"Session updated: {session_key} set to True for user: {user_id}")
    else:
        logging.info(f"User {user_id} has already been welcomed. No message sent.")
