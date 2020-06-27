import logging
import random

from flask import (
    jsonify,
    request,
)
from flask_cors import cross_origin
from flask_socketio import emit

from app import db, socketio
from app.main import blp
from app.models import Table, User
# from .mq import RabbitMQImpl
# from .sockets import GameplayNamespace


STARTING_STACK_SIZE = 1000


# table management endpoints


@blp.route("/monitoring")
def monitoring():
    from app.tasks import add_together
    import pdb
    pdb.set_trace()
    result = add_together.delay(24, 33)
    return {"ok": True, "sum": result.wait()}


@blp.route("/restart")
def restart():
    logging.info("sending a message to a client")

    Table.query.delete()
    User.query.delete()

    table = Table()
    players = [
        User(name=name, stack_size=1000, position=i)
        for i, name in enumerate(["aaa", "bbb", "ccc", "ddd", "eee"], 1)
    ]
    table.players = players

    db.session.add(table)
    db.session.add_all(players)

    table_id = table.id

    players = [
        {
            "position": player.position,
            "username": player.name,
            "stack": player.stack_size,
        }
        for player in table.players
    ]

    button_position = 1
    pot = 100

    # {
    #     "id": self.id,
    #     "button_position": 1,  # todo: button position

    #     "players": ,
    # }

    socketio.emit(
        "json",
        {
            "event": "preflop",
            "table_id": table_id,
            "blinds": {"small": 10, "big": 20, "ante": 2},
            "players": players,
            "active_players": players,
            "button_position": button_position,
            "pot": pot,
            "current": {"cards": ["As", "9h"]},
        },
    )
    # socketio.sleep(1)

    socketio.emit(
        "json",
        {"event": "flop_cards", "table_id": table_id, "flop_cards": ["2h", "9c", "Qs"]},
    )
    # socketio.sleep(5)

    socketio.emit("json", {"event": "turn_card", "turn_card": "Jh"})
    # socketio.sleep(1)

    socketio.emit("json", {"event": "river_card", "river_card": "7d"})

    socketio.emit(
        "json", {"event": "winner", "table_id": "555", "winner_position": 5, "pot": 150}
    )

    socketio.emit(
        "json",
        {
            "event": "request_action",
            "table_id": "234",
            "username": "Neo",
            "action_space": [
                {"type": "fold"},
                {"type": "check"},
                {"type": "call", "size": 120},
                {"type": "raise", "min": 555, "max": 1150},
            ],
        },
    )

    # socketio.sleep(1)

    # start_games()
    return "ok"


@socketio.on("connected")
def response():
    logging.info("received a message")


def send_socket_messages_to_client():
    logging.info("sending a message to a client")
    emit("hello_client", "hello world")


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


def get_random_free_position(table: Table) -> int:
    taken_positions = {player.position for player in table.players}
    free_positions = list(set(range(7)) - taken_positions)
    position = random.choice(free_positions)
    return position


@blp.route("/tables/<int:table_id>/join/<string:username>/", methods=["GET", "POST"])
def join_table(table_id: int, username: str):
    # if "username" not in session:
    #     return {"status": "error", "error": "login first", "session": str(session)}
    table = Table.query.filter(Table.id == table_id).one_or_none()
    # username = session.get("username")
    player = User.query.filter(User.name == username).one_or_none()
    if player is None:
        position = get_random_free_position(table)
        player = User(name=username, stack_size=STARTING_STACK_SIZE, position=position)

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


# game endpoints


@blp.route("/inform/<string:table_id>/<string:username>/", methods=["POST"])
def inform_user(table_id, message):
    message_json = request.get_json()

    # TODO: send to one player, not to all
    emit("some_event", "hello")
    # emit(  message_json)
    return "inform one"


@blp.route("/inform/<string:table_id>", methods=["POST"])
def inform_all_users(table_id: int):
    message = request.get_json()
    logging.debug(message)
    # emit(message)  # todo:
    return "inform all "


@blp.route("/request_action/<string:table_id>/<string:username>/", methods=["POST"])
def request_action(table_id, username):
    message_json = request.get_json()

    # {'event': 'preflop', 'table_id': 'vegas', 'players': [{'username': 'k', 'stack_size': 998, 'position': 2, 'cards': ('8h', '7h')}, {'username': 'k;lkl', 'stack_size': 978, 'position': 5, 'cards': ('4s', '7d')}, {'username': 'aa', 'stack_size': 998, 'position': 1, 'cards': ('Qs', 'Jh')}, {'username': 'iop', 'stack_size': 988, 'position': 3, 'cards': ('Qc', 'Ah')}], 'active_players': [1, 2, 3, 5], 'button_position': 2, 'current_pot': 38}

    # TODO: send to one player, not to all
    # emit(message_json)
    return "request action"


@blp.route("/act/<string:table_id>/<string:username>", methods=["POST"])
def act(table_id: int, username: str):
    # rabb/itmq TODO:
    return "ok"

# todo: send `new player joined table` in socket.
