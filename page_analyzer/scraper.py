import requests
from requests.exceptions import RequestException
from typing import Tuple, Optional


def request_to_url(url: str) -> Tuple[Optional[int], Optional[str]]:
    """
    Sends a GET request to the given URL and returns the status code
    and response text.

    :param url: URL to send the GET request to.
    :return: Tuple containing the status code and response text
    (if successful, else None).
    """
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise RequestException
        return response.status_code, response.text
    except RequestException:
        return None, None
