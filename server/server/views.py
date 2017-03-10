from server import db
from flask import request
from sqlalchemy import exc
from server.models import Server
from server.server import server
from server.discord import send_error_message


@server.route('/<uuid:server_key>', methods=['POST'])
def update_server_information(server_key):
    """
    Updates the server object with what maps it is currently on. This is useful for when a new record gets set, we know
    which servers to send an update recording command to.
    :return: doesn't really return anything, just a 200 status code
    """

    map_name = request.form.get('map')

    server = Server.query.filter_by(serverKey=str(server_key)).first()

    if server is None:
        return "Bad server Key", 400

    if map_name is None:
        return "No map specified", 400

    server.currentMap = map_name

    try:
        db.session.add(server)
        db.session.commit()
    except exc.SQLAlchemyError:
        send_error_message(f'Something went wrong when updating server {server_key}')
        return "Something went wrong", 400

    return "ok", 200
