import os
import logging
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from bot import create_app
from bot.commands import handle_search_alumni
from bot.events import handle_message_event
from config import Config
from slackeventsapi import SlackEventAdapter

app, slack_event_adapter, slack_client, bot_id = create_app()

# for debugging purpose
# can also serve as a welcome message
welcome_message = '''
Welcome to the MCIT Alumni Search Bot!
'''
# Send the welcome message only when the app is running in the main process
# something specific in the debug mode
if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    slack_client.chat_postMessage(channel='#test', text=welcome_message)


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
    return handle_search_alumni(request, slack_client)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
