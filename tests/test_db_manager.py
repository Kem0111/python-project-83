import pytest
import psycopg2
from unittest.mock import MagicMock, patch
from page_analyzer.db_manager import DBManager


@pytest.fixture
def mock_conn():
    conn = MagicMock(spec_set=psycopg2.connect)
    yield conn


@pytest.fixture
def db_manager(mock_conn):
    return DBManager(mock_conn)


def with_mock_execute_query(test):
    def wrapper(db_manager, *args, **kwargs):
        with patch.object(db_manager,
                          "_DBManager__execute_query") as mock_execute_query:
            test(db_manager, mock_execute_query=mock_execute_query,
                 *args, **kwargs)

    return wrapper


@with_mock_execute_query
def test_add_url_existing(db_manager, mock_execute_query):
    mock_execute_query.return_value = (1,)
    url_id, exists = db_manager.add_url("https://www.example.com")
    assert url_id == 1
    assert exists is True


@with_mock_execute_query
def test_add_url_new(db_manager, mock_execute_query):
    mock_execute_query.side_effect = [None, (1,)]
    url_id, exists = db_manager.add_url("https://www.example.com")
    assert url_id == 1
    assert exists is False


@with_mock_execute_query
def test_add_check(db_manager, mock_execute_query):
    data = (1, 200, "Test H1", "Test Title", "Test Description")
    db_manager.add_check(data)
    mock_execute_query.assert_called_with(
        db_manager._DBManager__QUERY['add_check'], data
    )


@with_mock_execute_query
def test_get_url_by_id(db_manager, mock_execute_query):
    url_id = 1
    expected_result = (1, "https://www.example.com", "2023-04-05")
    mock_execute_query.return_value = expected_result
    result = db_manager.get_url_by_id(url_id)
    assert result == expected_result
    mock_execute_query.assert_called_with(
        db_manager._DBManager__QUERY['get_url_by_id'], (url_id,), fetch='one'
    )


@with_mock_execute_query
def test_get_check_url(db_manager, mock_execute_query):
    mock_execute_query.return_value = [(1, 200, "Test H1", "Test Title",
                                        "Test Description", "2023-04-05")]
    url_id = 1
    expected_result = [
        (1, 200, "Test H1", "Test Title", "Test Description", "2023-04-05")
    ]
    result = db_manager.get_check_url(url_id)
    assert result == expected_result
    mock_execute_query.assert_called_with(
        db_manager._DBManager__QUERY['get_check_url'], (url_id,), fetch='all'
    )


@with_mock_execute_query
def test_get_all_urls(db_manager, mock_execute_query):
    expected_result = [
        (1, "https://www.example.com", "2023-04-05", 200)
    ]
    mock_execute_query.return_value = expected_result
    result = db_manager.get_all_urls()
    assert result == expected_result
    mock_execute_query.assert_called_with(
        db_manager._DBManager__QUERY['get_urls'], fetch='all'
    )
