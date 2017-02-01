from flask import Flask
#from server.config import Config
from server.servers import Servers
from server.models import db
from config import config


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # app.servers = servers

    from server.main import main
    app.register_blueprint(main)

    from server.api import api
    app.register_blueprint(api, url_prefix="/api")

    from server.replays import replays
    app.register_blueprint(replays, url_prefix="/replays")

    db.init_app(app)

    return app