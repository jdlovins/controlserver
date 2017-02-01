from flask import Blueprint

main = Blueprint('main', __name__)

# more cyclic imports
from . import views