import logging
from logging.config import dictConfig
import time

from app import socketio
from app.models import Table
from app.mq import RabbitMQImpl
from flask import request
from flask_socketio import emit, send

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)


rabbitmq = RabbitMQImpl()


def start_games():
    # wait_ping("http://0.0.0.0:5000")
    # time.sleep(5)
    logging.info("start games")

    from backend import app

    with app.app_context():
        for table in Table.query.all():
            start_hand(table)


def start_hand(table):
    # emit('message1','hello message11')

    key = ""
    message = table.as_json()
    logging.info("published " + message)
    rabbitmq.publish(message)


@socketio.on("connect")
def socketio_connect():
    print("connect ")
    logging.info("connect really???")


@socketio.on("message")
def message(message):
    import pdb

    pdb.set_trace()
    print("received message: ", message)
    send(message)


@socketio.on("some-event")
def some_test_event(data):
    logging.info("received message ", data)
    emit("message1", {"data": 42})


@socketio.on("act")
def act(data):

    print("message ", data)
    logging.info("message ", data)


@socketio.on("disconnect")
def disconnect():
    print("disconnect MINE")
    logging.info("disconnect MINE")


def send_to_client():
    print("message wil be sent")
    time.sleep(2)
    emit(f"customEmit", {"a": "message"}, broadcast=True)


# socketio.on_namespace(GameplayNamespace("/socket.io"))
