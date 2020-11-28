import os
import psycopg2

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300
    SECRET_KEY = os.environ["TOKEN"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def connect():
    connection = psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")
    return connection
