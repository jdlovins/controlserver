from server.api import api
from flask import current_app, request
from server.discord import send_discord_message


@api.route('/<uuid:server_key>/update', methods=['POST'])
def update_server_information(server_key):
    """
    Updates the server object with what map it is currently on. This is useful for when a new record gets set, we know
    which servers to send an update recording command to.
    :return: doesn't really return anything, just a 200 status code
    """
    map = request.form.get('map')

    server = current_app.servers.get_server_by_id(server_key)

    if server is None:
        return "Bad server UUID", 400

    if map is None:
        return "No map specified", 400

    server.map = map

    return "ok", 200


@api.route('/discord/send', methods=['POST'])
def discord_send_message():
    """
    Pushes a message to the discord webhook
    :return: success or failure depending on the result
    """

    message = request.form.get('message')

    payload = f'[Control Server] - {message}'

    if send_discord_message(payload):
        return "success", 200
    else:
        return "failure", 400


