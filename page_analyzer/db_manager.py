from pathlib import Path
from dotenv import load_dotenv
import os
import psycopg2
from typing import List, Optional, Tuple, Union

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


class DBManager:
    _QUERY = {
        'add_url': (
            "INSERT INTO urls (name, created_at)\n"
            "VALUES (%s, NOW()) RETURNING id"
        ),
        'get_url_id': "SELECT id FROM urls WHERE name = %s",
        'get_url_by_id': "SELECT id, name, created_at FROM urls WHERE id = %s",
        'get_urls': (
            """
            SELECT
            urls.id, urls.name, MAX(url_checks.created_at),
            url_checks.status_code
            FROM urls
            LEFT JOIN url_checks ON urls.id = url_checks.url_id
            GROUP BY urls.id, urls.name, url_checks.status_code
            ORDER BY urls.id DESC
            """
        ),
        'add_check': (
            "INSERT INTO url_checks "
            "(url_id, status_code, h1, title, description, created_at)\n"
            "VALUES (%s, %s, %s, %s, %s, NOW())"
        ),
        'get_check_url': (
            "SELECT id, status_code, h1, title, description, created_at\n"
            "FROM url_checks WHERE url_id = %s"
        )
    }

    def _execute_query(self, query: str, params: Optional[Tuple] = None,
                       fetch: Optional[str] = None) -> Union[List, Tuple, None]:
        """
        Executes a query using the given query string and parameters.

        :param query: Query string to be executed.
        :param params: Tuple containing parameters for the query.
        :param fetch: Specify 'one' to fetch one row, 'all' to fetch all rows,
        and None for no fetching.
        :return: Returns a tuple or a list of tuples based on the fetch
        parameter, or None if no fetching is performed.
        """

        with psycopg2.connect(DATABASE_URL) as self.conn:

            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                if fetch == 'one':
                    result = cursor.fetchone()
                elif fetch == 'all':
                    result = cursor.fetchall()
                else:
                    result = None
                    self.conn.commit()

        return result

    def create_tables(self) -> None:
        """Creates tables by executing SQL script from the 'database.sql'."""

        project_root = Path(__file__).resolve().parents[1]
        database_file_path = project_root / "database.sql"

        with open(database_file_path, "r") as file:
            create_tables_query = file.read()
        self._execute_query(create_tables_query)

    def get_url_by_id(self, url_id: int) -> Tuple[int, str, str]:
        """Returns URL information by its ID."""

        return self._execute_query(self._QUERY['get_url_by_id'],
                                   (url_id,), fetch='one')

    def add_url(self, url: str) -> Tuple[int, bool]:
        """Adds a URL to the database or returns its ID if it already exists."""

        result = self._execute_query(self._QUERY['get_url_id'],
                                     (url,), fetch='one')
        if result:
            url_id = result[0]
        else:
            url_id = self._execute_query(self._QUERY['add_url'],
                                         (url,), fetch='one')[0]
        return url_id, bool(result)

    def add_check(self, data: Tuple[int, int, str, str, str]) -> None:
        """
        Adds a check for a given URL.

        :param data: Tuple containing
        (url_id, status_code, h1, title, description)
        """
        self._execute_query(self._QUERY['add_check'], data)

    def get_check_url(self, url_id: int) -> List[Tuple[int, int, str,
                                                       str, str, str]]:
        """
        Retrieves check information for a given URL by its ID.

        :param url_id: URL ID to fetch check information for.
        :return: List of check information tuples.
        """
        return self._execute_query(self._QUERY['get_check_url'],
                                   (url_id,), fetch='all')

    def get_all_urls(self) -> List[Tuple[int, str, str, int]]:
        """
        Retrieves all URLs and their corresponding check information.

        :return: List of tuples containing URL and check information.
        """
        return self._execute_query(self._QUERY['get_urls'], fetch='all')
