"""Use blueprint"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api')

from .pets import *
from .users import *
