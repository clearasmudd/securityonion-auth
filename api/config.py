import os

APP_NAME = 'SO Auth'

# Keys
SECRET_KEY = os.environ.get('SECRET_KEY', 'YAJA6FZYZAVKACI3')
REFRESH_TOKEN_TIMEOUT = os.environ.get('REFRESH_TOKEN_TIMEOUT', 30)  # this is in days
AUTH_TOKEN_TIMEOUT = os.environ.get('TOKEN_TIMEOUT', 60)  # this is in minutes
CSRF_ENABLED = True

# ORM config
SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI', 'sqlite:///db.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False
