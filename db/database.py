import psycopg2
from config import Config

def connect_db():
    """
    Establishes a connection to the PostgreSQL database.

    Returns:
        connection: A connection object to interact with the database.
    """
    return psycopg2.connect(Config.DATABASE_URL)

def fetch_all_data():
    """
    Fetch All data from the PostgreSQL database.

    Returns:
        list: A list of tuples containing all alumni information.
    """
    conn = connect_db()
    cur = conn.cursor()
    query = "SELECT * FROM example_table"
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def fetch_alumni_info(role, limit=10):
    """
    Fetches alumni information from the database based on the specified role and limit.

    Args:
        role (str): The job title or role to filter alumni.
        limit (int): The maximum number of records to fetch.

    Returns:
        list: A list of tuples containing alumni information.
    """
    conn = connect_db()
    cur = conn.cursor()
    query = "SELECT name, current_company FROM alumni WHERE job_title = %s LIMIT %s"
    cur.execute(query, (role, limit))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
