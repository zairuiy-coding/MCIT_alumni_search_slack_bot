import os
from flask import request, jsonify
from bot import create_app
from bot.commands import process_command
from bot.events import handle_message_event

app, slack_event_adapter, slack_client, bot_id = create_app()

@slack_event_adapter.on('app_home_opened')
def app_home_opened(event_data):
    """
    Handles the event when the bot is added to the workspace.
    Sends a welcome message to the user who added the bot.
    """
    event = event_data.get('event', {})
    user_id = event.get('user')

    welcome_message = '''
    Welcome to the MCIT Alumni Search Bot!
    Please use the `/search-alumni` command followed by your query to find relevant alumni information.
    '''
    slack_client.chat_postMessage(channel=user_id, text=welcome_message)



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
    process_command(data, slack_client)  # Async processing in `process_command`
    return jsonify(response_type='in_channel', text="Your request is being processed...")

if __name__ == '__main__':
    app.run(debug=True, port=3000)
