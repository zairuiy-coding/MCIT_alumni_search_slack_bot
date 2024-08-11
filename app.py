import os
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from bot.commands import handle_search_alumni
from config import Config
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    Config.SIGNING_SECRET, '/slack/events', app)

slack_client = WebClient(token=Config.SLACK_BOT_TOKEN)

# get the id of our bot
BOT_ID = slack_client.api_call("auth.test")['user_id']

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
    # print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    # dummy message handling logic: echo back the user's text
    if user_id != BOT_ID:
        slack_client.chat_postMessage(channel=channel_id, text=text)

@app.route('/search-alumni', methods=['POST'])
async def search_alumni():
    """
    Endpoint to handle incoming Slack commands.

    Returns:
        Response: JSON response acknowledging the command.
    """
    return await handle_search_alumni(request, slack_client)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
