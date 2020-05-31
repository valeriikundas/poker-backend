from config import Config
from app import create_app

import pytest


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


@pytest.fixture
def app():
    app = create_app()
    return app


def test():
    assert True
