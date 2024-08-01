from flask import Flask, request, jsonify
from bot.commands import handle_slack_command
from config import Config

app = Flask(__name__)

@app.route('/slack/commands', methods=['POST'])
def slack_commands():
    """
    Endpoint to handle incoming Slack commands.

    Returns:
        Response: JSON response acknowledging the command.
    """
    return handle_slack_command(request)

if __name__ == '__main__':
    app.run(port=3000)
