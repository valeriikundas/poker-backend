from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.errors import blp as error_blp  # isort:skip

    app.register_blueprint(error_blp)

    from app.auth import blp as auth_blp  # isort:skip

    app.register_blueprint(auth_blp)

    from app.main import blp as main_blp  # isort:skip

    app.register_blueprint(main_blp)


from app import models  # isort:skip
