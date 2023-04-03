from urllib.parse import urlparse, urlunparse


def normalize_url(url):
    parsed_url = urlparse(url)
    normalized_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc.lower(),
        parsed_url.path.rstrip('/'),
        parsed_url.params,
        parsed_url.query,
        parsed_url.fragment
    ))
    return normalized_url
