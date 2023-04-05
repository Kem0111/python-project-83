from page_analyzer.html_parser import parse_html_content


def test_parse_html_content_with_all_tags():
    html = """
    <html>
        <head>
            <meta name="description" content="Test description">
            <title>Test title</title>
        </head>
        <body>
            <h1>Test h1</h1>
        </body>
    </html>
    """
    expected_result = ('Test h1', 'Test title', 'Test description')
    assert parse_html_content(html) == expected_result


def test_parse_html_content_without_h1_tag():
    html = """
    <html>
        <head>
            <meta name="description" content="Test description">
            <title>Test title</title>
        </head>
        <body>
        </body>
    </html>
    """
    expected_result = (None, 'Test title', 'Test description')
    assert parse_html_content(html) == expected_result


def test_parse_html_content_without_title_tag():
    html = """
    <html>
        <head>
            <meta name="description" content="Test description">
        </head>
        <body>
            <h1>Test h1</h1>
        </body>
    </html>
    """
    expected_result = ('Test h1', None, 'Test description')
    assert parse_html_content(html) == expected_result


def test_parse_html_content_without_meta_tag():
    html = """
    <html>
        <head>
            <title>Test title</title>
        </head>
        <body>
            <h1>Test h1</h1>
        </body>
    </html>
    """
    expected_result = ('Test h1', 'Test title', None)
    assert parse_html_content(html) == expected_result


def test_parse_html_content_with_empty_string():
    html = ""
    expected_result = (None, None, None)
    assert parse_html_content(html) == expected_result
