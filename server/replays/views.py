import os
import json
from flask import current_app, request, Response, send_file
from server.replays import replays
from server.models import Replay, Server, db
from server.helpers import push_recording_to_servers
from server.discord import send_error_message


@replays.route('/<int:replay_id>', methods=['POST', 'PUT', 'GET', 'DELETE'])
def upload_replay(replay_id):

    replay = Replay.query.filter_by(recordingID=replay_id).first()

    if replay is None:
        return "Invalid replay id", 400

    server_key = request.form.get('server_key')

    if request.method == "GET":

        filename = replay.get_file_name()
        path = os.path.join(current_app.config['REPLAY_FOLDER'], filename)

        if not os.path.exists(os.path.join(current_app.root_path, path)):
            return "Replay file does not exist", 400

        return send_file(path, as_attachment=True, attachment_filename=filename)

    if request.method == "POST" or request.method == "PUT":

        if 'replay' not in request.files:
            return "recording not found in the request", 400

        file = request.files['replay']

        length = request.form.get('length')

        server = Server.query.filter_by(serverKey=server_key).first()

        if server_key is None or server is None:
            return "invalid server key", 400

        filename = replay.get_file_name()

        path = os.path.join(current_app.root_path, current_app.config['REPLAY_FOLDER'], filename)

        try:
            file.save(path)
        except IOError as e:
            error = f'Error when saving file ({path}). Error Number: {e.errno}. Error: ({e.strerror})'

            send_error_message(error)
            return "failure", 400

        # fix this to use server_key
        # push_recording_to_servers(replay_id, server_id)

        replay.isUploaded = True
        replay.length = length
        db.session.add(replay)
        db.session.commit()

        return "success", 200

    if request.method == "DELETE":


        server = Server.query.filter_by(serverKey=server_key).first()

        if server_key is None or server is None:
            return "invalid server key", 400

        replay.isDeleted = True

        db.session.add(replay)
        db.session.commit()

        return "success", 200


@replays.route('/list', methods=['GET'])
def list_replays():
    """
    This gets all of the replays
    :return: A JSON formatted array
    """

    replay_list = json.dumps({"data": [replay.to_dict() for replay in Replay.query.all()]}, indent=4)
    return Response(response=replay_list, status=200, mimetype="application/json")


@replays.route('/<int:replay_id>/info', methods=['GET'])
def replay_info(replay_id):
    """
    This gets information about a specific replay
    :param replay_id: the ID of the replay
    :return: A JSON formatted string
    """

    replay = Replay.query.filter_by(recordingID=replay_id).first()

    if replay is None:
        return "invalid recording ID", 400
    else:
        data = json.dumps({"data": replay.to_dict()}, indent=4)
        return Response(response=data, status=200, mimetype="application/json")
