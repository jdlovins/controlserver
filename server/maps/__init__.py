from flask import Blueprint

maps = Blueprint('maps', __name__)

# more cyclic imports
from . import views