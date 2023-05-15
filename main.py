import json
from os.path import splitext

import requests

from src.cli import parse_args
from src.db.db import clean_cache, get_cache, init_db, insert_cache
from src.libs.swapi import handle_character_response, swapi_search
from src.libs.visualization import visualize


def search_task(search_query: str, world: str):
    """
    Perform a search for a Star Wars character using the SWAPI and handle the response.

    Args:
        search_query (str): The search query to use.
        world (str): Whether to retrieve homeworld information (True or False).

    Returns:
        None.
    """
    _id, response, hits, timestamp = get_cache(search_query)
    response = json.loads(response) if response else None
    save = False
    if response is None:
        response = swapi_search(search_query)
        save = True
    handle_character_response(search_query, response, world, save, _id, hits, timestamp)


def main():
    init_db()
    args = parse_args()
    if args.task == "search":
        if not args.query:
            print("Query parameter cannot be empty")
        search_task(args.query.strip(), args.world)

    elif args.task == "cache":
        if not args.clean:
            print("Cache option cannot be empty")
        clean_cache()
    elif args.task == "plot":
        filename, extension = splitext(args.output)
        if extension != ".png":
            raise ValueError("Output file must have png extension")
        visualize(args.output)
    else:
        print(
            "Invalid task, please refer to the command-line tool's '--help' manual for valid options."
        )


if __name__ == "__main__":
    main()
