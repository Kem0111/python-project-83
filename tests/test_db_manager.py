import pytest
import psycopg2
from unittest.mock import MagicMock
from page_analyzer.db_manager import DBManager


@pytest.fixture
def mock_conn():
    conn = MagicMock(spec_set=psycopg2.connect)
    yield conn


@pytest.fixture
def db_manager(mock_conn):
    return DBManager(mock_conn)


def test_add_url_existing(db_manager):
    db_manager._DBManager__execute_query = MagicMock(return_value=(1,))
    url_id, exists = db_manager.add_url("https://www.example.com")
    assert url_id == 1
    assert exists is True


def test_add_url_new(db_manager):
    db_manager._DBManager__execute_query = MagicMock(side_effect=[None, (1,)])
    url_id, exists = db_manager.add_url("https://www.example.com")
    assert url_id == 1
    assert exists is False


def test_add_check(db_manager):
    db_manager._DBManager__execute_query = MagicMock()
    data = (1, 200, "Test H1", "Test Title", "Test Description")
    db_manager.add_check(data)
    db_manager._DBManager__execute_query.assert_called_with(
        db_manager._DBManager__QUERY['add_check'], data
    )
