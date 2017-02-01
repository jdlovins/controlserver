from flask import Blueprint

replays = Blueprint('replays', __name__)

# more cyclic imports
from . import views