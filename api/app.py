import os

from flask import Flask
from flask_cors import CORS

from models import db
from routes import users, auth, req_utils
from scheduler import scheduler


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # init ORM
    with app.app_context():
        db.init_app(app)
        db.create_all()

    # init scheduler
    with app.app_context():
        scheduler.init_app(app)
        scheduler.start()

    app.register_blueprint(auth.blueprint)
    app.register_blueprint(users.blueprint)
    app.register_blueprint(req_utils.blueprint)

    CORS(app)

    return app


if __name__ == '__main__':
    so_auth = create_app()
    so_auth.run()
