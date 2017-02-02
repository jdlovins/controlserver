from flask import current_app
from server.models import Replay, Server


def push_recording_to_servers(replay_id):
    replay = Replay.query.filter_by(recordingID=replay_id).first()
    servers = Server.query.filter_by(currentMap=replay.map.name, isBotEnalbed=True).all()
    for server in servers:
        print("hey this recording belongs here")