from flask import request, jsonify
from slack_sdk import WebClient
from config import Config
from bot.nlp import interpret_user_query
from bot.responses import generate_response
from db.database import fetch_alumni_info

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
    
    response_url = data.get('response_url')
    processed_query = interpret_user_query(command_text)
    role = processed_query.get("role")
    limit = processed_query.get("limit", 10)
    
    results = fetch_alumni_info(role, limit)
    response_text = generate_response(results)
    
    slack_client.chat_postMessage(channel=data.get('channel_id'), text=response_text)
    
    return jsonify(response_type='ephemeral', text="Processing your request...")
