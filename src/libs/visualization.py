import sqlite3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.db.db import get_db


def get_responses_data(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Retrieves data from the CACHE table in the given SQLite database connection
    and returns a pandas dataframe containing the number of queries and the type
    of response for each query result.

    Args:
        conn: A connection object to the SQLite database.

    Returns:
        A pandas dataframe with two columns:
            - NumQueries: the number of queries for each response type.
            - QueryResult: the type of response ('No Response' or 'Response').

    """
    try:
        return pd.read_sql_query(
            "SELECT SUM(HITS) AS NumQueries, CASE WHEN RESPONSE <> '[]' THEN 'No Response' ELSE 'Response' END AS QueryResult FROM CACHE GROUP BY QueryResult",
            conn,
        )
    except Exception as e:
        raise Exception("An error occurred while executing the SQL query: ", e)


def get_searches_data(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Retrieves data from the CACHE table in the given SQLite database connection
    and returns a pandas dataframe containing the number of searches per day.

    Args:
        conn: A connection object to the SQLite database.

    Returns:
        A pandas dataframe with two columns:
            - date: the date of the search.
            - num_searches: the number of searches for that date.

    """
    try:
        return pd.read_sql_query(
            "SELECT DATE(timestamp) as date, COUNT(*) as num_searches FROM CACHE GROUP BY DATE(timestamp)",
            conn,
        )
    except Exception as e:
        raise Exception("An error occurred while executing the SQL query: ", e)


def get_most_popular_queries(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Retrieves data from the CACHE table in the given SQLite database connection
    and returns a pandas dataframe containing the top 10 most popular queries.

    Args:
        conn: A connection object to the SQLite database.

    Returns:
        A pandas dataframe with two columns:
            - QUERY: the query string.
            - HITS: the number of times the query was made.

    """
    try:
        return pd.read_sql_query(
            "SELECT QUERY, HITS FROM CACHE GROUP BY QUERY ORDER BY HITS DESC LIMIT 10",
            conn,
        )
    except Exception as e:
        raise Exception("An error occurred while executing the SQL query: ", e)


def get_most_popular_characters(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Retrieves data from the CACHE table in the given SQLite database connection
    and returns a pandas dataframe containing the top 10 most popular character names
    from the responses.

    Args:
        conn: A connection object to the SQLite database.

    Returns:
        A pandas dataframe with two columns:
            - name: the name of the character.
            - HITS: the number of times the character appeared in the responses.

    """
    try:
        return pd.read_sql_query(
            "SELECT json_extract(RESPONSE, '$.name') AS name, HITS FROM CACHE WHERE RESPONSE <> '[]' GROUP BY name ORDER BY HITS DESC LIMIT 10",
            conn,
        )
    except Exception as e:
        raise Exception("An error occurred while executing the SQL query: ", e)


def get_time_of_day_data(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Retrieves data from the CACHE table in the given SQLite database connection
    and returns a pandas dataframe containing the number of searches made per hour.

    Args:
        conn: A connection object to the SQLite database.

    Returns:
        A pandas dataframe with two columns:
            - hour: the hour of the day (in 24-hour format).
            - num_searches: the number of searches made during that hour.

    """
    try:
        return pd.read_sql_query(
            "SELECT strftime('%H', TIMESTAMP) AS hour, COUNT(*) AS num_searches FROM CACHE GROUP BY hour",
            conn,
        )
    except Exception as e:
        raise Exception("An error occurred while executing the SQL query: ", e)


def visualize(output_path: str) -> None:
    """
    Retrieve data from SQLite database and creates multiple visualizations using matplotlib.

    Args:
        output_path (str): Path to output the plot.

    Returns:
        None
    """
    # Get data from SQLite database
    with get_db() as conn:
        responses_df = get_responses_data(conn)
        searches_df = get_searches_data(conn)
        df_query = get_most_popular_queries(conn)
        df_name = get_most_popular_characters(conn)
        time_df = get_time_of_day_data(conn)

    fig, axs = plt.subplots(3, 2, figsize=(12, 12))
    axs[1, 0].axis("off")
    axs[1, 1].axis("off")
    axs[1, :] = plt.subplot(312)

    cmap = plt.get_cmap("plasma")

    # Searches made per day
    colors = cmap(np.linspace(0, 1, len(searches_df)))
    axs[0][0].bar(searches_df["date"], searches_df["num_searches"], color=colors)
    axs[0][0].set_xlabel("Date")
    axs[0][0].set_ylabel("Number of searches")
    axs[0][0].set_title("Searches made per day")

    # The query results statistics
    colors = cmap(np.linspace(0, 1, len(responses_df)))
    axs[0][1].pie(
        responses_df["NumQueries"],
        labels=responses_df["QueryResult"],
        autopct="%1.1f%%",
        colors=colors,
    )
    axs[0][1].set_title("Query Results")

    # Searches made by hour of day
    colors = cmap(np.linspace(0, 1, len(time_df)))
    axs[1][0].bar(time_df["hour"], time_df["num_searches"], color=colors)
    axs[1][0].set_xlabel("Hour of day")
    axs[1][0].set_ylabel("Number of searches")
    axs[1][0].set_title("Searches made by hour of day")

    # The most popular searched queries
    colors = cmap(np.linspace(0, 1, len(df_query)))
    x_ticks = np.arange(len(df_query))
    axs[2][0].bar(x_ticks, df_query["HITS"], color=colors)
    axs[2][0].set_xticks(x_ticks)
    axs[2][0].set_xticklabels(df_query["QUERY"], rotation=45, ha="right")
    axs[2][0].set_ylabel("Number of searches")
    axs[2][0].set_title("Most popular searched queries")

    # The most popular character's name from the response
    x_ticks = np.arange(len(df_name))
    colors = cmap(np.linspace(0, 1, len(df_name)))
    axs[2][1].bar(x_ticks, df_name["HITS"], color=colors)
    axs[2][1].set_xticks(x_ticks)
    axs[2][1].set_xticklabels(df_name["name"], rotation=45, ha="right")
    axs[2][1].set_ylabel("Number of occurrences")
    axs[2][1].set_title("Most common character names in responses")

    plt.subplots_adjust(hspace=0.7, wspace=0.5)

    plt.savefig(output_path, bbox_inches="tight", pad_inches=0.2)
