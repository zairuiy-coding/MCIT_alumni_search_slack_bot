
import logging
from flask import request, jsonify
import redis
from bot import create_app
from bot.commands import handle_search_alumni
from bot.events import handle_message_event
from config import Config

app, slack_event_adapter, slack_client, bot_id, celery = create_app()

# Initialize Redis client outside of the function
redis_client = redis.StrictRedis.from_url(Config.REDIS_URL)

@slack_event_adapter.on('app_home_opened')
def app_home_opened(event_data):
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
        welcome_message = '''
        Welcome to the MCIT Alumni Search Bot!
        Please use the `/search-alumni` command followed by your query to find relevant alumni information.
        '''
        slack_client.chat_postMessage(channel=user_id, text=welcome_message)

        # Set the key in Redis to mark that the user has been welcomed
        redis_client.set(session_key, "True", ex=Config.REDIS_EXPIRATION_TIME)
        logging.info(f"Session updated: {session_key} set to True for user: {user_id}")
    else:
        logging.info(f"User {user_id} has already been welcomed. No message sent.")


    
@slack_event_adapter.on('message')
def message(payload):
    """
    Handles incoming messages in Slack. Forwards the message event to the event handler.
    
    Args:
        payload (dict): The event payload from Slack containing details of the message.
    """
    event = payload.get('event', {})
    handle_message_event(event, bot_id, slack_client)

    
@app.route('/search-alumni', methods=['POST'])
def search_alumni():
    """
    Endpoint to handle incoming Slack commands.

    Returns:
        Response: JSON response acknowledging the command.
    """
    data = request.form
    handle_search_alumni.delay(data)  # Async processing with Celery
    return jsonify(response_type='in_channel', text="Your request is being processed...")

if __name__ == '__main__':
    app.run(debug=True, port=3000)
