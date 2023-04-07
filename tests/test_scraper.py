from unittest.mock import MagicMock, patch
from page_analyzer.scraper import request_to_url
from requests.exceptions import RequestException


def test_request_to_url_success():
    with patch("requests.get") as mock_get:
        mock_get.return_value = MagicMock(status_code=200, text="Test content")
        status_code, text = request_to_url("https://www.example.com")

    assert status_code == 200
    assert text == "Test content"


def test_request_to_url_error():
    with patch("requests.get") as mock_get:
        mock_get.side_effect = RequestException()
        status_code, text = request_to_url("https://www.example.com")

    assert status_code is None
    assert text is None


def test_request_to_url_not_found():
    with patch("requests.get") as mock_get:
        mock_get.return_value = MagicMock(status_code=404, text="Not Found")
        status_code, text = request_to_url("https://www.example.com")

    assert status_code is None
    assert text is None

