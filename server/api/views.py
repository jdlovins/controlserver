from server.api import api
from flask import request
from server.discord import send_discord_message


@api.route('/discord', methods=['POST'])
def discord_send():
    """
    Pushes a message to the discord webhook
    :return: success or failure depending on the result
    """

    message = request.form.get('message')

    if message is None:
        return "No message specified", 400

    payload = f'[Control Server] - {message}'

    if send_discord_message(payload):
        return "success", 200
    else:
        return "failure", 400


