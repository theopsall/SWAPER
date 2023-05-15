from datetime import datetime
from json import dumps
from typing import Optional

from src.db.db import get_cache, insert_cache, update_cache, update_hits_cache
from src.utils.swapi_utils import swapi_request, swapi_search


def handle_character_response(
    query: str,
    response: dict,
    world: bool = False,
    save: bool = True,
    query_id: Optional[int] = None,
    hits: Optional[int] = 0,
    timestamp: Optional[str] = None,
) -> None:

    """
    Handles the response from the Star Wars API for a given character.

    Args:
    query (str): The search query used to get the character.
    response (dict): The response from the Star Wars API for the character.
    world (bool, optional): Whether to include information about the character's homeworld. Defaults to False.
    save (bool, optional): Whether to save the response in the cache. Defaults to True.
    query_id (int, optional): The ID of the cache entry to update. Defaults to None.
    timestamp (str, optional): The timestamp of the cache entry to update. Defaults to None.

    Returns:
    None.

    Raises:
    None.
    """
    if response:
        print(f"Name: {response['name']}")
        print(f"Height: {response['height']}")
        print(f"Mass: {response['mass']}")
        print(f"Bith: {response['birth_year']}")

        if world:
            if save:
                homeland_reponse = swapi_request(url=response["homeworld"])
            else:
                should_update = "rotation_period" not in response["homeworld"]
                if should_update:
                    homeland_reponse = swapi_request(url=response["homeworld"])
                    response["homeworld"] = homeland_reponse
                    update_cache(query_id, dumps(response), hits + 1, datetime.now())
                else:
                    homeland_reponse = response["homeworld"]

            handle_homeland_response(homeland_reponse)
            response["homeworld"] = homeland_reponse

        if save:
            insert_cache(query, dumps(response), datetime.now())
        else:
            update_hits_cache(query_id, hits + 1, datetime.now())
            print(f"cached: {timestamp}")
    else:
        if save:
            insert_cache(query, dumps(response), datetime.now())
        else:
            update_hits_cache(query_id, hits + 1, datetime.now())
        print("The force is not strong within you")


def handle_homeland_response(response: dict) -> None:
    """
    Prints information about a Star Wars planet response obtained from the Star Wars API (SWAPI).

    Args:
        response (dict): A dictionary containing the response data from SWAPI for a planet.

    Returns:
        None.

    Raises:
        None.

    The function prints the following information about the planet:
    - Name
    - Population
    - Length of year and day in Earth time (in years and days).

    Example usage:
    >>> response = swapi_request("https://swapi.dev/api/planets/1/")
    >>> handle_homeland_response(response)
    """
    print("\n" * 2)
    print("HomeWorld")
    print("-" * len("HomeWorld"))
    print(f"Name: {response['name']}")
    print(f"Population: {response['population']}")

    homeworld_year = int(response["orbital_period"]) / 365
    homeworld_day = int(response["rotation_period"]) / 24
    print(
        f"On {response['name']}, 1 year on Earth is {homeworld_year:.2f} years and 1 day is {homeworld_day:.2f} Earth days."
    )
