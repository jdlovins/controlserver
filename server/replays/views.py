from server.replays import replays
from flask import current_app, request, Response
from server.models import Replay
from werkzeug.utils import secure_filename
from server.helpers import push_recording_to_servers
import os
import uuid

import json
# these routes are actually /replays/upload, /replays/download, /replays/list


@replays.route('/<int:replay_id>', methods=['POST', 'PUT'])
def upload_replay(replay_id):

    if 'replay' not in request.files:
        return "recording not found in the request", 400

    file = request.files['replay']

    server_key = uuid.UUID(request.form.get('server_key'))

    server = current_app.servers.get_server_by_id(server_key)

    if server_key is None or server is None:
        return "invalid server key", 400

    filename = secure_filename(file.filename)

    if server.type == "surf":
        path = os.path.join(current_app.config['SURF_FOLDER'], filename)
    else:
        path = os.path.join(current_app.config['BHOP_FOLDER'], filename)

    file.save(path)

    push_recording_to_servers(replay_id)

    return "success", 200


@replays.route('/<int:replay_id>', methods=['GET'])
def download_replay(replay_id):
    pass


@replays.route('/list', methods=['GET'])
def list_replays():
    """
    :return: A JSON formatted array of all the replays
    """
    replays = json.dumps([replay.to_dict() for replay in Replay.query.all()], indent=4)
    return Response(response=replays, status=200, mimetype="application/json")


@replays.route('/<int:map_id>/list', methods=['GET'])
def list_replay_by_map(map_id):
    """
    :param map_id: the ID of the map
    :return: A JSON formatted array of all the replays matching the map_id
    """
    replays = json.dumps([replay.to_dict() for replay in Replay.query.filter_by(mapID=map_id).all()], indent=4)
    return Response(response=replays, status=200, mimetype="application/json")


@replays.route('/<int:replay_id>/info', methods=['GET'])
def replay_info(replay_id):
    """
    :param replay_id: the id of the replay
    :return: A JSON formatted string of the replay matching the ID
    """
    replay = Replay.query.filter_by(recordingID=replay_id).first()
    if replay is None:
        error = json.dumps({
            "error": "Invalid recording ID",
            "error_code": 200
        })
        return Response(response=error, status=400, mimetype="application/json")
    else:
        data = json.dumps(replay.to_dict())
        return Response(response=data, status=200, mimetype="application/json")
