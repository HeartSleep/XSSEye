import base64

from flask import Blueprint, make_response, url_for, request
from werkzeug.exceptions import abort

from . import payloads
from ..users.login import verify_password

routes = Blueprint('public_api', __name__)


def check_post_args(*args):
    for arg in args:
        if arg not in request.form:
            return False
    return True


@routes.before_request
def auth_check():
    if request.method != 'POST':
        abort(405)
    if not check_post_args('_username', '_password') or \
            not verify_password(request.form['_username'], request.form['_password']):
        abort(403)


@routes.route('/payloads/get_url', methods=['POST'])
def get_payload_url():
    if not check_post_args('hostname', 'port', 'protocol', 'request_base64'):
        abort(406)
    uid = payloads.generate_payload(
        request.form['hostname'],
        request.form['port'],
        request.form['protocol'],
        base64.b64decode(request.form['request_base64'])
    )
    resp = make_response(url_for('generator.show', uid=uid, _external=True))
    resp.headers.add('Content-Type', 'text/plain')
    return resp
