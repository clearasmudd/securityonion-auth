import socket

from flask import Blueprint, request, jsonify, current_app as app

from routes.constants import UNHANDLED_EXCEPTION_RESPONSE

blueprint = Blueprint('utils', __name__, url_prefix='/utils')


@blueprint.route('/check-local', methods=["POST"])
def check_local():
    try:
        if request.remote_addr == '127.0.0.1':
            return jsonify({
                'status': 'success',
                'message': 'Request is local'
            }), 200
        else:
            return jsonify({
                'status': 'fail',
                'message': 'Request is not local'
            }), 401
    except Exception as e:
        app.logger.error(e)
        return jsonify(UNHANDLED_EXCEPTION_RESPONSE), 500
