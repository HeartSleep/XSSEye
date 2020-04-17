from core import Static
from core.users.login import get_user


def get_reports_hosts():
    user_info = get_user()
    if user_info is None:
        return False

    with Static.psql.cursor() as cursor:
        #  TODO: Need refactor sql query
        if user_info['is_admin']:
            cursor.execute("""
            SELECT reports.hostname FROM xsseye.reports WHERE id_payload IN (
                SELECT payloads.id FROM xsseye.payloads
            ) AND reports.hostname IS NOT NULL GROUP BY reports.hostname
            """)
        else:
            cursor.execute("""
            SELECT reports.hostname FROM xsseye.reports WHERE id_payload IN(
                SELECT payloads.id FROM xsseye.payloads WHERE id_owner=%(user_id)s
            ) GROUP BY reports.hostname
            """, {
                'user_id': user_info['id']
            })
        return [x[0] for x in cursor.fetchall()]
