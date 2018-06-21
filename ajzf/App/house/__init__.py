from flask import Blueprint

house = Blueprint('house', __name__)

from . import house_views
