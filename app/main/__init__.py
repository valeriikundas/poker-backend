from flask import Blueprint

blp = Blueprint("main", __name__, url_prefix="/app")

from app.main import views  # isort:skip
