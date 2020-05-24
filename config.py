import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "my-very-secret-key"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
