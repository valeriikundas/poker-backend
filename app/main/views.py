import logging
import threading
import time

import requests
from flask import (
    current_app,
    escape,
    jsonify,
    render_template,
    request,
    session,
    url_for,
)
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO

from app.main import blp
from app.models import Table, User
from app import db

# from .mq import RabbitMQImpl
# from .sockets import GameplayNamespace

STARTING_STACK_SIZE = 1000

# table management endpoints


@blp.route("/monitoring")
def monitoring():
    return {"ok": True}


@blp.route("/tables")
def tables():
    return jsonify(
        [
            {
                "id": table.id,
                "players": [
                    {
                        "id": player.id,
                        "username": player.name,
                        "stack_size": player.stack_size,
                        "position": player.position,
                    }
                    for player in table.players
                ],
            }
            for table in Table.query.all()
        ]
    )


@blp.route("/table", methods=["POST", "GET"])
def create_table():
    table = Table(name="vegas")
    db.session.add(table)
    db.session.commit()
    return {"id": table.id}


@blp.route("/tables/<int:table_id>/join/<string:username>/", methods=["GET", "POST"])
def join_table(table_id: int, username: str):
    # if "username" not in session:
    #     return {"status": "error", "error": "login first", "session": str(session)}
    table = Table.query.filter(Table.id == table_id).one_or_none()
    # username = session.get("username")
    player = User.query.filter(User.name == username).one_or_none()
    if player is None:
        player = User(name=username, stack_size=STARTING_STACK_SIZE)

    table.players.append(player)
    db.session.add(player)
    db.session.commit()
    return {"status": "joined"}


@blp.route("/tables/<int:table_id>/leave/<string:username>/", methods=["get", "post"])
def leave_table(table_id: int, username: str):
    # FIXME: this will not work for multitabling

    # if "username" not in session:#todo: only for logged in users
    #     return {"status": "login first"}
    # username = session.get("username")
    player = User.query.filter(User.name == username).one_or_none()
    table = Table.query.get(table_id)
    table.players.remove(player)
    db.session.commit()
    return {"status": "left table"}


@blp.route("/tables/<string:table_id>/")
@cross_origin()
def table(table_id):
    table = Table.query.get(table_id)
    pot = 0
    players = [
        {
            "id": player.id,
            "username": player.name,
            "stack_size": player.stack_size,
            "position": player.position,
        }
        for player in table.players
    ]
    return {"status": "game", "pot": pot, "players": players}


