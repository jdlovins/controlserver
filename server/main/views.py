from server.main import main


@main.route('/ping')
def ping():
    return "pong", 200
