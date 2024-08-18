

from db import get_db_connection


def fetch_all_data():
    """
    Fetch All data from the PostgreSQL database.

    Returns:
        list: A list of tuples containing all alumni information.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM alumni_table")
            results = cur.fetchall()
    return results