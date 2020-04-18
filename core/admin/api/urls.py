from flask import Blueprint, jsonify

from . import reports

routes = Blueprint('admin_api', __name__)


@routes.route('/get_reports/<hostname>')
def get_reports(hostname):
    return jsonify(reports.get_all(hostname))
