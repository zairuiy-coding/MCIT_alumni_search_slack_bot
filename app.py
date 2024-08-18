
import logging
from flask import request, jsonify
import redis
from bot import create_app
from bot.commands.search_alumni import handle_search_alumni
from bot.events.app_home_open import handle_app_home_opened_event
from bot.events.message import handle_message_event
from config import Config

app, slack_event_adapter, slack_client, bot_id, celery = create_app()

@slack_event_adapter.on('app_home_opened')
def app_home_opened(event_data):
    """
    Handles the event when the bot is added to the workspace.
    Sends a welcome message to the user who added the bot.
    """
    handle_app_home_opened_event(event_data)

    
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
