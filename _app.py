import logging
import threading
import time

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
import requests

from .mq import RabbitMQImpl
from .sockets import GameplayNamespace


CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")


STARTING_STACK_SIZE = 10000


def init_db():
    Player.objects.delete()
    Table.objects.delete()

    player1 = Player(username="John", stack_size=3000, position=4).save()
    player2 = Player(username="Will", stack_size=2000, position=2).save()
    player3 = Player(username="Robert", stack_size=3500, position=7).save()
    Table(name="default", players=[player1, player2, player3]).save()


init_db()


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


# @socketio.on("connect")
# def socketio_connect():
#     print("connect ")


# @socketio.on("act")
# def act(data):
#     print("message ", data)


# @socketio.on("disconnect")
# def disconnect():
#     print("disconnect ")


# def send_to_client():
#     print("message wil be sent")
#     time.sleep(2)
#     socketio.emit(f"customEmit", {"a": "message"}, broadcast=True)


if __name__ == "__main__":
    threading.Thread(target=start_games).start()  # temporary
    app.run()
    #    socketio.on_namespace(GameplayNamespace("/socket.io"))
    # socketio.run(app, host="0.0.0.0")

