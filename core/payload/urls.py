from flask import Blueprint, abort, make_response, url_for

from core import Static

routes = Blueprint('generator', __name__)


@routes.route('/x<uid>', methods=['GET', 'POST'])
def show(uid):
    resp = make_response(Static.generator.generate({
        'uid': uid,
        'callback_url': url_for('reports.xss_report', uid=uid, _external=True)
    }))
    resp.headers.add('Content-Type', 'text/javascript')
    return resp

