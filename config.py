import os


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost:5432/poker"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "secret!"
    DEBUG = True
