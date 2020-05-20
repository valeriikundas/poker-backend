from flask import Blueprint

blp = Blueprint("auth", __name__, url_prefix="/auth")

from app.auth import views  # isort:skip
