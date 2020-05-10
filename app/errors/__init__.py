from flask import Blueprint

blp = Blueprint("errors", __name__)

from app.errors import handlers  # isort:skip
