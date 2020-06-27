import os


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost:5432/poker"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "secret!"
    DEBUG = True
    CELERY_BROKER_URL = "redis://localhost:6379"
    CELERY_RESULT_BACKEND = "redis://localhost:6379"

