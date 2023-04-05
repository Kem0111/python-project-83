import requests
from requests.exceptions import RequestException


def request_to_url(url):
    try:
        response = requests.get(url)
        return response.status_code, response.text
    except RequestException:
        return None, None
