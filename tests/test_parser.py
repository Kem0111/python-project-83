from page_analyzer.parser import normalize_url
import pytest


@pytest.mark.parametrize("url, expected_normalized_url", [
    ("http://example.com", "http://example.com"),
    ("HTTP://Example.com/", "http://example.com"),
    ("https://example.com:80/path", "https://example.com:80/path"),
    ("https://example.com/path/", "https://example.com/path"),
    ("http://example.com/path?query=value", "http://example.com/path?query=value"),
    ("http://example.com/path#fragment", "http://example.com/path#fragment"),
    ("http://example.com/path?query=value#fragment", "http://example.com/path?query=value#fragment"),
])
def test_normalize_url(url, expected_normalized_url):
    assert normalize_url(url) == expected_normalized_url