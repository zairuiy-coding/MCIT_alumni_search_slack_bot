from flask import request, jsonify
from slack_sdk import WebClient
from config import Config
from bot.nlp import interpret_user_query
from bot.responses import generate_response
from db.database import fetch_alumni_info
from bot.nlp import process_data_with_openai
from db.database import fetch_all_data

slack_client = WebClient(token=Config.SLACK_BOT_TOKEN)

def handle_slack_command(request):
    """
    Handles Slack slash commands by processing the request and responding with relevant information.

    Args:
        request (Request): Incoming request from Slack.

    Returns:
        Response: JSON response indicating the command is being processed.
    """
    data = request.form
    command_text = data.get('text')

    # step 1: Pre-Fetch All Data from the Database
    all_records = fetch_all_data()

    # Step 2: fetch data and user qeury to OpenAI API
    api_response = process_data_with_openai(command_text, all_records)
    
    # Step 3: Generate and Post the Final Response
    slack_client.chat_postMessage(channel=data.get('channel_id'), text=api_response)
    
    return jsonify(response_type='ephemeral', text="Processing your request...")
