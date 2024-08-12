from flask import request, jsonify
from slack_sdk import WebClient

from config import Config
from bot.nlp import process_data_with_openai
from db.database import fetch_all_data

def handle_search_alumni(command_text, channel_id, slack_client):
    """
    Handles Slack slash commands by processing the request and responding with relevant information.

    Args:
        request (Request): Incoming request from Slack.

    Returns:
        Response: JSON response indicating the command is being processed.
    """
    # Ensure command_text is not None or empty
    if not command_text:
        command_text = "No specific query provided."

    # Acknowledge receipt of the command quickly to avoid timeouts
    slack_client.chat_postMessage(channel=channel_id, text=f"Searching for your request: {command_text}")

    # step 1: Pre-Fetch All Data from the Database
    all_records = fetch_all_data()

    # Step 2: fetch data and user qeury to OpenAI API
    api_response = process_data_with_openai(command_text, all_records)

    # Ensure api_response is not None or empty
    if not api_response:
        api_response = "No relevant alumni information found based on your query."
    
    # Step 3: Generate and Post the Final Response
    slack_client.chat_postMessage(channel=channel_id, text=api_response)
    
    # return jsonify(response_type='in_channel', text="Your request has been processed.")
