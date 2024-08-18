from contextlib import contextmanager

import psycopg2

from config import Config


@contextmanager
def get_db_connection():
    """
    Context manager to handle database connection.
    Ensures the connection is closed after use.
    """
    conn = psycopg2.connect(Config.DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()