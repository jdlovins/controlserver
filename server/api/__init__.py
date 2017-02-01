from flask import Blueprint

api = Blueprint('api', __name__)

# more cyclic imports
from . import views