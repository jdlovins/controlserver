import os
import json
from flask import current_app, request, Response, send_file
from sqlalchemy import func
from server.replays import replays
from server.models import Replay, Server, db
from server.helpers import push_recording_to_servers
from server.discord import send_error_message


@replays.route('/<int:replay_id>', methods=['POST', 'PUT', 'GET', 'DELETE'])
def upload_replay(replay_id):

    replay = Replay.query.filter_by(recordingID=replay_id).first()

    if replay is None:
        return "Invalid replay id", 400

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

        server_id = request.form.get('server_id')

        server = Server.query.filter_by(serverID=server_id).first()

        if server_id is None or server is None:
            return "invalid server id", 400

        filename = replay.get_file_name()

        path = os.path.join(current_app.root_path, current_app.config['REPLAY_FOLDER'], filename)

        try:
            file.save(path)
        except IOError as e:
            error = f'Error when saving file ({path}). Error Number: {e.errno}. Error: ({e.strerror})'

            send_error_message(error)
            return "failure", 400

        push_recording_to_servers(replay_id, server_id)

        replay.isUploaded = True
        db.session.add(replay)
        db.session.commit()

        return "success", 200

    if request.method == "DELETE":

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

    replay_list = json.dumps([replay.to_dict() for replay in Replay.query.all()], indent=4)
    return Response(response=replay_list, status=200, mimetype="application/json")


@replays.route('/<int:map_id>/list', methods=['GET'])
def list_replay_by_map(map_id):
    """
    This gets all of the replays for a specific map
    :param map_id: the ID of the map
    :return: A JSON formatted array
    """

    replay_list = json.dumps([replay.to_dict() for replay in Replay.query.filter_by(mapID=map_id).all()], indent=4)
    return Response(response=replay_list, status=200, mimetype="application/json")


@replays.route('/<int:map_id>/best', methods=['GET'])
def list_best_replays_by_map(map_id):
    """
    This gets the highest recording ID for each zone. In our system the highest should mean the newest and fastest
    :param map_id: the ID of the map
    :return: A JSON formatted array
    """

    best_replays = Replay.query.filter_by(mapID=map_id, isUploaded=True, isDeleted=False).filter(Replay.recordingID.in_(
        db.session.query(func.max(Replay.recordingID)).filter_by(mapID=map_id).group_by(Replay.stage, Replay.type)
    )).all()

    resp = json.dumps([replay.to_dict() for replay in best_replays], indent=4)
    return Response(response=resp, status=200, mimetype="application/json")


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
        data = json.dumps(replay.to_dict())
        return Response(response=data, status=200, mimetype="application/json")
