from flask import jsonify, request
from flask_login import current_user, login_user

from app.auth import blp
from app.models import User


@blp.route("/login", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return jsonify({"status": "ok"})
    username = request.json["username"]
    user = User.query.filter(User.name == username)
    login_user(user, remember=True)
    return jsonify({"status": "ok"})
