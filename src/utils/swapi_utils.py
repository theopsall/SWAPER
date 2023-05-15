import requests


def swapi_request(url: str) -> dict:
    """
    Sends a GET request to the specified URL and returns the response as a dictionary.

    Parameters:
        url (str): The URL to send the GET request to.

    Returns:
        dict: The response as a dictionary.

    Raises:
        requests.exceptions.HTTPError: If the GET request returns a non-2xx status code.
        SystemExit: If there is an error with the HTTP request.

    Example:
        To get information about a character from the Star Wars API:
        >>> url = "https://swapi.dev/api/people/1/"
        >>> response = swapi_request(url)
        >>> print(response)
        [{'name': 'Luke Skywalker', 'height': '172', 'mass': '77', 'hair_color': 'blond', ...}]
    """
    try:
        response = requests.get(url=url)
        response.raise_for_status()

    except requests.exceptions.Timeout as e:
        raise ValueError("Timeout occurred while making a request:", e)
    except requests.exceptions.ConnectionError as e:
        raise ValueError("Connection error occurred while making a request:", e)
    except requests.exceptions.RequestException as e:
        raise ValueError("Error occurred while making a request:", e)

    return response.json()


def swapi_search(search_query: str) -> dict:
    """
    Searches the Star Wars API for a character by name and returns their information as a dictionary.

    Parameters:
        search_query (str): The name of the character to search for.

    Returns:
        dict: The information about the character as a dictionary.

    Raises:
        requests.exceptions.HTTPError: If the GET request returns a non-2xx status code.
        SystemExit: If there is an error with the HTTP request, or if no character is found.

    Example:
        To search for information about Luke Skywalker:
        >>> search_query = "Luke Skywalker"
        >>> response = swapi_search(search_query)
        >>> print(response)
        {'name': 'Luke Skywalker', 'height': '172', 'mass': '77', 'hair_color': 'blond', ...}
    """
    url = f"https://swapi.dev/api/people/?search={search_query}"
    response = swapi_request(url=url)
    return response["results"][0] if response["count"] else []
