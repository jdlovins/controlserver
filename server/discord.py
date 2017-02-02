import requests
import json
from flask import current_app


def send_discord_message(message):
    url = current_app.config['DISCORD_WEBHOOK']

    headers = {'content-type': 'application/json'}
    data = json.dumps({
        'content': message
    })

    result = requests.post(url, data, headers=headers)

    if result.status_code == 204:
        return True
    else:
        return False

