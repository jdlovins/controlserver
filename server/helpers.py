import json
import requests
from server.models import Replay, Server
from flask import current_app


def push_recording_to_servers(replay_id, server_id):
    replay = Replay.query.filter_by(recordingID=replay_id).first()
    servers = Server.query.filter(Server.currentMap == replay.map.name, Server.isBotEnabled,
                                  Server.serverID != server_id).all()
    for server in servers:
        print("hey this recording belongs here")