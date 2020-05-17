import os

from flask import current_app


class BaseConfig:
    """Base configuration"""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0
    PASSWORD_TOKEN_EXPIRATION_SECONDS = 3600
    UPLOAD_FOLDER = os.path.join(current_app.root_path, 'uploads')
    PICTURE_ALLOWED_EXTENSIONS = {'jpg', 'png', 'gif'}
    ACTIVITY_ALLOWED_EXTENSIONS = {'gpx', 'zip'}
    TEMPLATES_FOLDER = os.path.join(current_app.root_path, 'email/templates')
    UI_URL = os.environ.get('UI_URL')
    EMAIL_URL = os.environ.get('EMAIL_URL')
    SENDER_EMAIL = os.environ.get('SENDER_EMAIL')


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = 'development key'
    USERNAME = 'admin'
    PASSWORD = 'default'
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    """Testing configuration"""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    SECRET_KEY = 'test key'
    USERNAME = 'admin'
    PASSWORD = 'default'
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 0
    TOKEN_EXPIRATION_SECONDS = 3
    PASSWORD_TOKEN_EXPIRATION_SECONDS = 3
    UPLOAD_FOLDER = '/tmp/fitTrackee/uploads'
