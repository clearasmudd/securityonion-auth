import re
from datetime import datetime

from flask import Blueprint, request, jsonify, current_app as app

from models.user import User
from routes.constants import UNHANDLED_EXCEPTION_RESPONSE, PASSWORD_REGEX, LOGIN_FAIL_RESPONSE
from routes.utils import save_model, requires_token, require_same_source_origin

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/', methods=["POST"])
@requires_token(token_type='auth')
def check_auth(user_id):
    # If we have reached the function that means the user authenticated successfully
    user: User = User.query.filter_by(id=user_id).first
    message: str = f'User {user.username} validated auth token at {datetime.now()}'
    app.logger.info(message)
    return jsonify({
        'status': 'success',
        'message': message
    }), 200


@blueprint.route('/register', methods=['POST'])
@require_same_source_origin
def register_user():
    try:
        content: dict = request.get_json()
        username: str = content.get('username')
        user: User = User.query.filter_by(username=username).first()
        if not user:
            password: str = content.get('password')

            if not re.match(PASSWORD_REGEX, password):
                return jsonify({
                    'status': 'fail',
                    'message': 'Password must be at least 6 characters'
                }), 400

            try:
                user: User = User(
                    username=username,
                    password=password
                )
                save_model(user)
                return jsonify({
                    'status': 'success',
                    'message': f'Created new user {user.username}'
                }), 200
            except Exception as e:
                app.logger.error(e)
                return jsonify(UNHANDLED_EXCEPTION_RESPONSE), 500
        else:
            return jsonify({
                'status': 'fail',
                'message': 'User already exists, please log in'
            }), 401

    except Exception as e:
        app.logger.error(e)
        return jsonify(UNHANDLED_EXCEPTION_RESPONSE), 500


@blueprint.route('/login', methods=['POST'])
def login():
    content: dict = request.get_json()
    try:
        user: User = User.query.filter_by(username=content.get('username')).first()
        if user is None:
            return jsonify(LOGIN_FAIL_RESPONSE), 401
        if not user.check_password(content.get('password')):
            app.logger.error(f'User {user.username} failed to login')
            user.failed_login_attempts += 1
            save_model(user)
            return jsonify(LOGIN_FAIL_RESPONSE), 401
        else:
            auth_token = User.encode_token(user.id, user.username)
            message: str = f'User {user.username} logged in at {user.last_login}'
            response = {
                'status': 'success',
                'message': message,
                'auth_token': auth_token.decode()
            }
            if content.get('remember_me', False):
                refresh_token = User.encode_token(user.id, user.username, is_refresh=True)
                user.current_refresh_token = refresh_token
                user.remember_me = True
                response['refresh_token'] = refresh_token.decode()
            user.logged_in = True
            user.last_login = datetime.now()
            user.failed_login_attempts = 0
            save_model(user)
            app.logger.info(message)
            return jsonify(response), 200

    except Exception as e:
        app.logger.error(e)
        return jsonify(UNHANDLED_EXCEPTION_RESPONSE), 500


@blueprint.route('/logout', methods=['POST'])
@requires_token(token_type='auth')
def logout(user_id):
    try:
        user: User = User.query.filter_by(id=user_id).first()
        user.logged_in = False
        user.last_logout = datetime.now()
        save_model(user)
        message = f'User {user.username} logged out at {user.last_logout}'
        app.logger.info(message)
        return jsonify({
            'status': 'success',
            'message': message
        }), 200

    except Exception as e:
        app.logger.error(e)
        return jsonify(UNHANDLED_EXCEPTION_RESPONSE), 500


@blueprint.route('/renew', methods=['POST'])
@requires_token(token_type='refresh')
def renew_auth_token(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        new_auth_token = User.encode_token(user_id, user.username)
        return jsonify({
            'status': 'success',
            'auth_token': new_auth_token.decode()
        }), 200

    except Exception as e:
        app.logger.error(e)
        return jsonify(UNHANDLED_EXCEPTION_RESPONSE), 500
