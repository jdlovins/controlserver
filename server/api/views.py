from server import db
from server.api import api
from flask import current_app, request, url_for
from server.discord import send_discord_message, send_error_message
from server.models import Server
from sqlalchemy import exc


@api.route('/<int:server_id>/update', methods=['POST'])
def update_server_information(server_id):
    """
    Updates the server object with what map it is currently on. This is useful for when a new record gets set, we know
    which servers to send an update recording command to.
    :return: doesn't really return anything, just a 200 status code
    """
    map = request.form.get('map')

    server = Server.query.filter_by(serverID=server_id).first()

    if server is None:
        return "Bad server ID", 400

    if map is None:
        return "No map specified", 400

    server.currentMap = map

    try:
        db.session.add(server)
        db.session.commit()
    except exc.SQLAlchemyError:
        send_error_message(f'Something went wrong when updating server {server_id}')
        return "Something went wrong", 400

    return "ok", 200


@api.route('/discord/send', methods=['POST'])
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


