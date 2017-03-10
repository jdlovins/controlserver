from flask import Flask
from server.models import db
from config import config


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from server.main import main
    app.register_blueprint(main)

    from server.api import api
    app.register_blueprint(api, url_prefix="/api")

    from server.replays import replays
    app.register_blueprint(replays, url_prefix="/replays")

    from server.server import server
    app.register_blueprint(server, url_prefix="/servers")

    from server.maps import maps
    app.register_blueprint(maps, url_prefix="/maps")

    db.init_app(app)

    return app
