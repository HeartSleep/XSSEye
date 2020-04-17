from werkzeug.security import check_password_hash

from core import Static


def verify_password(username, password):
    user_info = get_user(username)
    if user_info is None:
        return False

    return check_password_hash(user_info['password'], password)


def get_user(username=None):
    if username is None:
        username = Static.auth.username()
    with Static.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM users.user WHERE username=%(username)s",
            {
                'username': username
            }
        )
        return cursor.fetchone()


def get_user_id(username=None):
    if username is None:
        username = Static.auth.username()
    with Static.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM users.user WHERE username=%(username)s",
            {
                'username': username
            }
        )
        row = cursor.fetchone()
        if row is not None and 'id' in row:
            return row['id']
        return None
