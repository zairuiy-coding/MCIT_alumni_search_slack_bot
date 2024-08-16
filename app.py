
import logging
from flask import request, jsonify, session
from bot import create_app
from bot.commands import handle_search_alumni
from bot.events import handle_message_event

app, slack_event_adapter, slack_client, bot_id, celery = create_app()

@slack_event_adapter.on('app_home_opened')
def app_home_opened(event_data):
    """
    Handles the event when the bot is added to the workspace.
    Sends a welcome message to the user who added the bot.
    """
    event = event_data.get('event', {})
    user_id = event.get('user')

    if not session.get(f'welcomed_{user_id}'):
        welcome_message = '''
        Welcome to the MCIT Alumni Search Bot!
        Please use the `/search-alumni` command followed by your query to find relevant alumni information.
        '''
        slack_client.chat_postMessage(channel=user_id, text=welcome_message)
        
        # Mark the user as welcomed in the session
        session[f'welcomed_{user_id}'] = True

    logging.info(f"App home opened by user: {user_id}")


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
