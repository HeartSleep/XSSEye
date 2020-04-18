import hashlib

from flask import Blueprint, render_template, abort, send_from_directory

from ..admin.view import *

routes = Blueprint('admin', __name__)


@routes.route('/')
def dashboard():
    return render_template('index.html')


@routes.route('/screenshot/<uuid:uuid>')
def get_screenshot(uuid):
    path = '%s.png' % (uuid,)
    if path is None:
        abort(404)
    return send_from_directory('screenshots', path)


@routes.route('/reports')
def reports():
    hosts = get_reports_hosts()
    return render_template('reports.html', hosts=hosts, md5=lambda s: hashlib.md5(s.encode()).hexdigest())
