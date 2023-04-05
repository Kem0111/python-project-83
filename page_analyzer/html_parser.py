from bs4 import BeautifulSoup


def parse_html_content(text):
    soup = BeautifulSoup(text, 'html.parser')
    description = soup.find('meta', attrs={'name': 'description'})

    return (
        getattr(soup.find('h1'), 'text', None),
        getattr(soup.title, 'text', None),
        description.get('content', None) if description else None
    )
