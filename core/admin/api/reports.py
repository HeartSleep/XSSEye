from ...static import Static
from ...users.login import get_user


def get_all(hostname):
    user_info = get_user()
    if user_info is None:
        return False

    column_names = []
    with Static.psql.cursor() as cursor:
        #  TODO: Need refactor sql query
        cursor.execute("""
        SELECT reports.* FROM xsseye.reports WHERE id_payload IN(
            SELECT payloads.id FROM xsseye.payloads WHERE id_owner=%(user_id)s
        ) AND hostname=%(hostname)s
        """, {
            'user_id': user_info['id'],
            'hostname': hostname
        })
        for desc in cursor.description:
            column_names.append(desc[0])

        def handle_row(row):
            row = dict(zip(column_names, row))
            url = ('https' if row['is_https'] else 'http') + '://' + \
                  row['hostname'] + \
                  (
                      ''
                      if (row['is_https'] and row['port'] == 443) or (not row['is_https'] and row['port'] == 80)
                      else ':' + str(row['port'])
                  ) + '/' + row['path'].lstrip('/') + \
                  ('?' + row['query'] if row['query'] is not None and len(row['query']) > 0 else '') + \
                  ('#' + row['hash'] if row['hash'] is not None and len(row['hash']) > 0 else '')
            row['humanize'] = {
                'url': url
            }
            return row

        return [handle_row(x) for x in cursor.fetchall()]
