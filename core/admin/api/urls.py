from flask import Blueprint, jsonify, request
from werkzeug.exceptions import abort

from . import reports
from ...static import Static
from ...users.login import get_user

routes = Blueprint('admin_api', __name__)


@routes.route('/get_reports/<hostname>')
def get_reports(hostname):
    return jsonify(reports.get_all(hostname))


@routes.route('/mark_report', methods=['MARK'])
def mark_report():
    if not request.is_json:
        abort(405)
    data = request.get_json()
    if 'uniq_id' not in data or 'mark' not in data:
        abort(405)
    user_info = get_user()
    if user_info is None:
        abort(403)
    with Static.psql.cursor() as cursor:
        try:
            cursor.execute("""
            UPDATE xsseye.reports 
                SET is_marked=%(is_marked)s 
                WHERE 
                    uniq_id=%(uniq_id)s AND 
                    EXISTS (
                        SELECT FROM xsseye.payloads 
                        WHERE id_owner=%(user_id)s AND id=id_payload
                    )
            """, {
                'user_id': user_info['id'],
                'uniq_id': data['uniq_id'],
                'is_marked': data['mark']
            })
        except Exception:
            abort(500)
    return jsonify({'status': 'ok'})


@routes.route('/delete_report', methods=['DELETE'])
def delete_report():
    if not request.is_json:
        abort(405)
    data = request.get_json()
    if 'uniq_id' not in data:
        abort(405)
    user_info = get_user()
    if user_info is None:
        abort(403)
    with Static.psql.cursor() as cursor:
        try:
            cursor.execute("""
            DELETE FROM xsseye.reports 
                WHERE 
                    uniq_id=%(uniq_id)s AND 
                    EXISTS (
                        SELECT FROM xsseye.payloads 
                        WHERE id_owner=%(user_id)s AND id=id_payload
                    )
            """, {
                'user_id': user_info['id'],
                'uniq_id': data['uniq_id']
            })
        except Exception:
            abort(500)
    return jsonify({'status': 'ok'})
