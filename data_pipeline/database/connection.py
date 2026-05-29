
# import psycopg2
# from config import settings

# def get_connection():
#     return psycopg2.connect(settings.database_url)

from psycopg2.pool import ThreadedConnectionPool
from config import settings

_pool = ThreadedConnectionPool(minconn=1, maxconn=10, dsn=settings.database_url)

def get_connection():
    return _pool.getconn()

def put_connection(conn):
    _pool.putconn(conn)