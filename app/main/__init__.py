from flask import Blueprint

blp = Blueprint("main", __name__, url_prefix="/api")

from app.main import views, sockets  # isort:skip
