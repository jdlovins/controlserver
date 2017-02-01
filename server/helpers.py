from flask import current_app
from server.models import Replay


def push_recording_to_servers(replay_id):
    replay = Replay.query.filter_by(recordingID=replay_id).first()
    for server in current_app.servers.servers:
        if server.map == replay.map.name:
            print("hey this recording belongs here")