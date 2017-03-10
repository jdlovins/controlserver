from flask import Blueprint

server = Blueprint('server', __name__)

# more cyclic imports
from . import views