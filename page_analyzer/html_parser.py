from bs4 import BeautifulSoup
from typing import Tuple, Optional


def parse_html_content(text: str) -> Tuple[Optional[str],
                                           Optional[str], Optional[str]]:
    """
    Parses the HTML content and extracts the H1, title, and description.

    :param text: HTML content as a string.
    :return: Tuple containing H1, title, and description (if present, else None)
    """
    soup = BeautifulSoup(text, 'html.parser')
    description = soup.find('meta', attrs={'name': 'description'})

    return (
        getattr(soup.find('h1'), 'text', None),
        getattr(soup.title, 'text', None),
        description.get('content', None) if description else None
    )
