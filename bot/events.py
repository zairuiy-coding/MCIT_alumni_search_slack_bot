
import logging
from slack_sdk import WebClient

def handle_message_event(event, bot_id, slack_client):
    """
    Handles Slack message events by sending a prompt message to the channel, 
    advising the user to use the `/search-alumni` slash command.

    Args:
        event (dict): The event data containing details of the Slack message.
        bot_id (str): The bot's user ID to prevent the bot from responding to its own messages.
        slack_client (WebClient): The Slack WebClient instance for sending messages.
    """
    channel_id = event.get('channel')
    user_id = event.get('user')
    user_text = event.get('text')

    # Log the user ID
    logging.info(f"User ID: {user_id}")
    logging.info(f"User text: {user_text}")

    prompt_text = '''
        Please use the `/search-alumni` slash command to search for your query
    '''
    
    # Send the prompt text if the message isn't from the bot, is not a slash command, and user_id is not None
    if user_id is not None and user_id != bot_id and (user_text is not None and not user_text.startswith('/')):
        slack_client.chat_postMessage(channel=channel_id, text=prompt_text)
