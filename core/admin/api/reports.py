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
        SELECT r.*, row_to_json(p.*) as payload FROM xsseye.reports r
        JOIN xsseye.payloads p
            ON r.hostname=%(hostname)s AND (r.id_payload=p.id) AND (p.id_owner=%(user_id)s)
        """, {
            'user_id': user_info['id'],
            'hostname': hostname
        })
        for desc in cursor.description:
            column_names.append(desc[0])

        def handle_row(row):
            row = dict(zip(column_names, row))
            url = row['protocol'] + '://' + \
                  row['hostname'] + \
                  (
                      ''
                      if (row['protocol'] == 'https' and row['port'] == 443) or
                         (row['protocol'] != 'https' and row['port'] == 80)
                      else ':' + str(row['port'])
                  ) + '/' + row['path'].lstrip('/') + \
                  ('?' + row['query'] if row['query'] is not None and len(row['query']) > 0 else '') + \
                  ('#' + row['hash'] if row['hash'] is not None and len(row['hash']) > 0 else '')
            row['humanize'] = {
                'url': url
            }
            return row

        return [handle_row(x) for x in cursor.fetchall()]
