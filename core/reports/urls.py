from flask import Blueprint, make_response

routes = Blueprint('reports', __name__)


@routes.route('/rx<uid>', methods=['GET', 'POST'])
def xss_report(uid):
    resp = make_response('Hi: ' + uid)
    resp.headers['Content-Type'] = 'text/javascript'
    return resp
