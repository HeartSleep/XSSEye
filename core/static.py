import psycopg2
import psycopg2.extras

from config import Config
from .payload.generator import Generator
from .utils.http_auth import HTTPBasicAuth


class Static:
    psql = psycopg2.connect(**Config.POSTGRES_CONNECTION_INFO)

    @staticmethod
    def cursor():
        Static.psql.autocommit = True
        return Static.psql.cursor(cursor_factory=psycopg2.extras.DictCursor)

    generator = Generator(Config.PAYLOAD_INCLUDING_SCRIPTS)
    auth = HTTPBasicAuth()
