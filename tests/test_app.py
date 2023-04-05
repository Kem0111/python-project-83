import pytest
from flask_testing import TestCase
from page_analyzer.app import app, db_manager
from unittest.mock import MagicMock


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


if __name__ == '__main__':
    pytest.main()
