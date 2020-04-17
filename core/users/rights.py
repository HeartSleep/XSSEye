from core import Static
from core.users.login import get_user


def user_have_right_to_domain(domain, username=None):
    user_info = get_user(username)
    if user_info is None:
        return False
    if user_info['is_admin'] or user_info['all_domains']:
        return True
    with Static.psql.cursor() as cursor:
        row = cursor.execute("""
        SELECT EXISTS (
            SELECT FROM users.domains_access WHERE id_user=%(user_id)s AND %(domain)s LIKE domain_pattern ESCAPE '\\'
        )
        """, {
            'domain': domain,
            'user_id': user_info['id']
        })
        return row.fetchone()[0]


def user_have_right_to_payload(uuid, username=None):
    user_info = get_user(username)
    if user_info is None:
        return False
    if user_info['is_admin']:
        return True
    with Static.psql.cursor() as cursor:
        row = cursor.execute("""
        SELECT EXISTS (
            SELECT FROM xsseye.payloads WHERE uniq_id=%(uuid)s AND id_owner=%(user_id)s
        )
        """, {
            'uuid': uuid,
            'user_id': user_info['id']
        })
        return row.fetchone()[0]


def user_have_right_to_report(uuid, username=None):
    user_info = get_user(username)
    if user_info is None:
        return False
    if user_info['is_admin']:
        return True
    with Static.psql.cursor() as cursor:
        row = cursor.execute("""
        SELECT EXISTS (
            SELECT FROM xsseye.payloads WHERE uniq_id=(
                SELECT id_payload FROM xsseye.reports WHERE uniq_id=%(uuid)s   
            ) AND id_owner=%(user_id)s
        )
        """, {
            'uuid': uuid,
            'user_id': user_info['id']
        })
        return row.fetchone()[0]
