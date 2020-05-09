"""
this api implements 2 things:
1. table and user management
2. game related stuff

table management consists of
 - authentication
 - players joining and leaving table

game related stuff is the minimal version. all work should be done by game server and clients
backend should just do mailing between game server and clients.
  - inform player - send info to one player at the table - ws
  - inform players - send info to all players at the table - ws
  - request_action from player - send request for move - ws
  - act - apply move from player - resend it to game server - http
"""

import logging
import threading
import time

import requests
import simplejson as json
from flask import (
    Flask,
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
from mongoengine import connect

from models import Player, Table
from mq import RabbitMQImpl
from sockets import GameplayNamespace

app = Flask(__name__)
app.secret_key = "secret!"
app.debug = True

connect("poker", host="mongodb")

CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")


STARTING_STACK_SIZE = 10000


def init():
    Player.objects.delete()
    Table.objects.delete()

    player1 = Player(username="John", stack_size=3000, position=4).save()
    player2 = Player(username="Will", stack_size=2000, position=2).save()
    player3 = Player(username="Robert", stack_size=3500, position=7).save()
    Table(name="default", players=[player1, player2, player3]).save()


init()


@app.route("/tables/")
def tables():
    return {
        "tables": list(
            map(
                lambda i: {"table_id": str(i.id), "players_count": len(i.players)},
                Table.objects.all(),
            )
        )
    }


@app.route("/users/")
def users():
    return Player.objects.to_json()


@app.route("/login/", methods=["POST"])
@cross_origin()
def login():
    try:
        username = request.json.get("username", None)
        if not username:
            return {
                "status": "error",
                "error": "request body does not contain username",
            }
        session["username"] = username
        player = Player.objects(username=username).first()
        if player is None:
            player = Player(username=username, stack_size=STARTING_STACK_SIZE).save()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.route("/logout/")
def logout():
    if "username" in session:
        del session["username"]
    return {"status": "logged out"}


@app.route("/tables/<string:username>/join/<string:table_id>/", methods=["GET"])
@cross_origin()
def join_table(username, table_id):
    # if "username" not in session:
    #     return {"status": "error", "error": "login first", "session": str(session)}
    table = Table.objects(id=table_id).first()
    # username = session.get("username")
    player = Player.objects(username=username).first()
    if player is None:
        player = Player(username=username, stack_size=STARTING_STACK_SIZE).save()
        table["players"].append(player)
        table.save()
    return {"status": "joined"}


@app.route("/tables/leave/")
def leave_table():
    # FIXME: this will not work for multitabling
    if "username" not in session:
        return {"status": "login first"}
    username = session.get("username")
    player = Player.objects.get(username=username)
    table = Table.objects.filter(players__contains=player)
    return {"status": "left table"}


@app.route("/tables/<string:table_id>/")
def table(table_id):
    table = Table.objects.get(id=table_id)
    pot = 0
    players = [
        {"username": i.username, "stack_size": i.stack_size, "position": i.position}
        for i in table.players
    ]
    return {"status": "game", "pot": pot, "players": players}


@app.route("/inform/<string:table_id>/<string:username>/", methods=["POST"])
def inform(table_id, message):
    message_json = request.get_json()

    # TODO: send to one player, not to all
    # emit(message_json)


@app.route("/request_action/<string:table_id>/<string:username>/", methods=["POST"])
def request_action(table_id, username):
    message_json = request.get_json()

    # TODO: send to one player, not to all
    # emit(message_json)


def wait_ping(host_port):
    while True:
        try:
            print(f"wait ping {host_port}")
            requests.get(host_port)
            return
        except:
            time.sleep(1)


def start_games():
    # wait_ping("http://0.0.0.0:5000")
    time.sleep(5)

    for table in Table.objects:
        start_hand(table)


def start_hand(table):
    rmq = RabbitMQImpl()
    key = ""
    message = table.as_json()
    print(message)
    rmq.publish(message)


@socketio.on("connect")
def socketio_connect():
    print("connect ")


@socketio.on("act")
def act(data):
    print("message ", data)


@socketio.on("disconnect")
def disconnect():
    print("disconnect ")


def send_to_client():
    print("message wil be sent")
    time.sleep(2)
    socketio.emit(f"customEmit", {"a": "message"}, broadcast=True)


if __name__ == "__main__":
    threading.Thread(target=start_games).start()
    #    socketio.on_namespace(GameplayNamespace("/socket.io"))
    socketio.run(app, host="0.0.0.0")
