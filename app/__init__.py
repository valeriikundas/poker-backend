import logging

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config
import requests
import time

logging.getLogger("flask_cors").level = logging.DEBUG


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


def wait_ping(host_port):
    while True:
        try:
            print(f"wait ping {host_port}")
            requests.get(host_port)
            return
        except Exception:
            time.sleep(1)


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # threading.Thread(target=start_games).start()  # temporary
    #    socketio.on_namespace(GameplayNamespace("/socket.io"))
    # socketio.run(app, host="0.0.0.0")

    # from app.errors import blp as error_blp  # isort:skip

    # app.register_blueprint(error_blp)

    from app.auth import blp as auth_blp  # isort:skip

    app.register_blueprint(auth_blp)

    from app.main import blp as main_blp  # isort:skip

    app.register_blueprint(main_blp)

    return app


from app import models  # isort:skip
