import json
from flask import Response, request
from server.maps import maps
from sqlalchemy import func
from server.models import Replay, db


@maps.route('/<int:map_id>/replays', methods=['GET'])
def list_replay_by_map(map_id):
    """
    This gets all of the replays for a specific maps
    :param map_id: the ID of the maps
    :return: A JSON formatted array
    """

    replay_list = json.dumps({"data": [replay.to_dict() for replay in
                                       Replay.query.filter_by(mapID=map_id).all()]}, indent=4)
    return Response(response=replay_list, status=200, mimetype="application/json")


@maps.route('/<int:map_id>/replays/best', methods=['GET'])
def list_best_replays_by_map(map_id):
    """
    This gets the highest recording ID for each zone. In our system the highest should mean the newest and fastest
    :param map_id: the ID of the maps
    :return: A JSON formatted array
    """

    zone_type = request.args.get('type')
    zone = request.args.get('zone')
    code = 200

    best_replays = Replay.query.filter_by(mapID=map_id).filter(Replay.recordingID.in_(
        db.session.query(func.max(Replay.recordingID)).filter_by(mapID=map_id,  isUploaded=True, isDeleted=False).
        group_by(Replay.stage, Replay.type)
    ))

    if zone_type is not None:
        best_replays = best_replays.filter_by(type=zone_type)

    if zone is not None:
        best_replays = best_replays.filter_by(stage=zone)

    best_replays = best_replays.all()

    if len(best_replays):
        resp = json.dumps({"data": [replay.to_dict() for replay in best_replays]}, indent=4)
    else:
        resp = None
        code = 204

    return Response(response=resp, status=code, mimetype="application/json")


