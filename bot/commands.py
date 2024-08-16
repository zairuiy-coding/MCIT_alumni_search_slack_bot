import random

from celery import shared_task
from flask import current_app

from bot.nlp import process_data_with_openai
from db.database import fetch_all_data

@shared_task(bind=True)
def handle_search_alumni(self, data):
    """ 
    Handles Slack slash commands by processing the request and responding with relevant information.

    Args:
        data (dict): Incoming data from Slack.
        slack_client (WebClient): The Slack WebClient instance for sending messages.
    """
    command_text = data.get('text')
    channel_id = data.get('channel_id')

    # Ensure command_text is not None or empty
    if not command_text:
        command_text = "No specific query provided."

    try:
        # step 1: Pre-Fetch All Data from the Database
        all_records = fetch_all_data()
        random.shuffle(all_records)
        # print("all_records: ", all_records)

        # Step 2: fetch data and user qeury to OpenAI API
        api_response = process_data_with_openai(command_text, all_records)

        # Ensure api_response is not None or empty
        if not api_response:
            api_response = "No relevant alumni information found based on your query."
        
        # Step 3: Generate and Post the Final Response
        # Accessing the Slack client within the Flask app context
        with current_app.app_context():
            slack_client = current_app.extensions['slack_client']
            slack_client.chat_postMessage(channel=channel_id, text=api_response)
    
    
    except Exception as e:
        with current_app.app_context():
            slack_client = current_app.extensions['slack_client']
            slack_client.chat_postMessage(channel=channel_id, text=f"An error occurred: {str(e)}")