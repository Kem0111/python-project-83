from flask_testing import TestCase
from page_analyzer.app import app, db_manager
from unittest.mock import MagicMock
from werkzeug.datastructures import MultiDict
from page_analyzer.scraper import request_to_url
from page_analyzer.html_parser import parse_html_content


class TestApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_index(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assert_template_used('index.html')

    def test_get_urls(self):
        db_manager.get_all_urls = MagicMock(return_value=[])
        response = self.client.get('/urls')
        self.assert200(response)
        self.assert_template_used('urls.html')

    def test_get_url(self):
        db_manager.get_url_by_id = MagicMock(
            return_value=(1, 'https://example.com', None)
        )
        db_manager.get_check_url = MagicMock(return_value=[])
        response = self.client.get('/urls/1')
        self.assert200(response)
        self.assert_template_used('url.html')

    def test_add_check_url(self):
        db_manager.add_check = MagicMock()
        request_to_url.return_value = (
            200, "<html><head><title>Test</title></head></html>"
        )
        parse_html_content.return_value = ("Test H1", "Test Title",
                                           "Test Description")

        data = MultiDict({'url': 'https://www.example.com'})
        response = self.client.post('/urls/1/checks', data=data,
                                    follow_redirects=True)
        self.assert200(response)
        self.assert_template_used('url.html')
        db_manager.add_check.assert_called()

    def test_add_url(self):
        db_manager.add_url = MagicMock(return_value=(1, False))
        data = MultiDict({'url': 'https://www.example.com'})
        response = self.client.post('/urls', data=data, follow_redirects=True)
        self.assert200(response)
        self.assert_template_used('url.html')
        db_manager.add_url.assert_called_with('https://www.example.com')
