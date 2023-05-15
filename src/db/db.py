import sqlite3
import sys
from os.path import dirname, join

from src.config import DATABASE
from src.utils.filesystem_utils import file_exists

DATABASE = join(dirname(__file__), DATABASE)


def get_db():
    """Connects to the SQLite database and returns a Connection object.

    Returns:
        sqlite3.Connection: A connection object to the SQLite database.

    Raises:
        Exception: If an error occurs while connecting to the database.
    """
    try:
        return sqlite3.connect(DATABASE)
    except (sqlite3.Error, sqlite3.Warning) as e:
        raise Exception(e)


def create_cache_table():
    """Creates the CACHE table in the SQLite database.

    Returns:
        None.
    """
    try:
        conn = get_db()
        conn.execute(
            """CREATE TABLE CACHE
                     (ID            INTEGER PRIMARY KEY AUTOINCREMENT,
                     QUERY          TEXT NOT NULL,
                     RESPONSE       TEXT NOT NULL,
                     TIMESTAMP      DATETIME NOT NULL,
                     HITS           INT NOT NULL DEFAULT 1
                     );"""
        )
        conn.close()
    except (sqlite3.Error, sqlite3.Warning) as e:
        raise Exception(e)


def insert_cache(query: str, response: str, timestamp: str) -> None:
    """Inserts a cache entry into the CACHE table.

    Args:
        query (str): The search query.
        response (str): The response to the search query.
        timestamp (str): The timestamp of the cache entry.

    Returns:
        None.
    """
    try:

        conn = get_db()
        conn.execute(
            "INSERT INTO CACHE (QUERY, RESPONSE, TIMESTAMP) VALUES (?, ?, ?);",
            (query, response, timestamp),
        )
        conn.commit()
        conn.close()
    except (sqlite3.Error, sqlite3.Warning) as e:
        raise Exception(e)


def update_cache(query_id: int, response: str, hits: int, timestamp: str) -> None:
    """Updates a cache entry in the CACHE table.

    Args:
        query_id (int): The ID of the cache entry to update.
        response (str): The new response to the search query.
        timestamp (str): The new timestamp of the cache entry.

    Returns:
        None.
    """
    try:
        conn = get_db()
        conn.execute(
            "UPDATE CACHE SET RESPONSE = ?, TIMESTAMP = ?, HITS =? WHERE ID = ?;",
            (response, timestamp, hits, query_id),
        )
        conn.commit()
        conn.close()
    except (sqlite3.Error, sqlite3.Warning) as e:
        raise Exception(e)


def update_hits_cache(query_id: int, hits: int, timestamp: str) -> None:
    """
    Update the HITS and TIMESTAMP columns in the CACHE table for the given query ID.

    Args:
        query_id (int): The ID of the query to update.
        hits (int): The new number of hits for the query.
        timestamp (str): The new timestamp for the query in the format "YYYY-MM-DD HH:MM:SS".

    Returns:
        None.
    """
    try:
        conn = get_db()
        conn.execute(
            "UPDATE CACHE SET HITS = ?, TIMESTAMP = ? WHERE ID = ?;",
            (hits, timestamp, query_id),
        )
        conn.commit()
        conn.close()
    except (sqlite3.Error, sqlite3.Warning) as e:
        raise Exception(e)


def get_cache(query: str) -> tuple:
    """Retrieves the cache entry matching the given search query.

    Args:
        query (str): The search query.

    Returns:
        tuple: A tuple containing the ID, response, and timestamp of the cache entry.
            If no cache entry is found, returns (None, None, None).
    """
    try:
        conn = get_db()
        cursor = conn.execute(
            f"""SELECT ID, RESPONSE, HITS, TIMESTAMP FROM CACHE WHERE QUERY LIKE '%{query}%' OR RESPONSE LIKE '%{query}%';"""
        )
        response = cursor.fetchone()
        conn.close()
    except (sqlite3.Error, sqlite3.Warning) as e:
        raise Exception(e)
    return response if response else (None, None, 0, None)


def clean_cache() -> None:
    """Deletes all entries in the CACHE table.

    Returns:
        None.
    """
    try:
        conn = get_db()
        cursor = conn.execute("DELETE  FROM CACHE;")
        conn.commit()
        conn.close()
    except (sqlite3.Error, sqlite3.Warning) as e:
        raise Exception(e)


def init_db() -> None:
    """Initializes the SQLite database by creating the CACHE table if it does not exist.

    Returns:
        None.
    """
    if not file_exists(DATABASE):
        try:
            with open(DATABASE, "w") as f:
                pass
        except Exception as e:
            raise Exception(e)
        create_cache_table()
