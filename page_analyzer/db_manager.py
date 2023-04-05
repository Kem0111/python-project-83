from pathlib import Path


class DBManager:
    __QUERY = {
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

    def __init__(self, conn):
        self.conn = conn

    def __execute_query(self, query, params=None, fetch=None):
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

    def create_tables(self):
        project_root = Path(__file__).resolve().parents[1]
        database_file_path = project_root / "database.sql"

        with open(database_file_path, "r") as file:
            create_tables_query = file.read()
        self.__execute_query(create_tables_query)

    def get_url_by_id(self, url_id):
        return self.__execute_query(self.__QUERY['get_url_by_id'],
                                    (url_id,), fetch='one')

    def add_url(self, url):
        result = self.__execute_query(self.__QUERY['get_url_id'],
                                      (url,), fetch='one')
        if result:
            url_id = result[0]
        else:
            url_id = self.__execute_query(self.__QUERY['add_url'],
                                          (url,), fetch='one')[0]
        return url_id, bool(result)

    def add_check(self, data):
        self.__execute_query(self.__QUERY['add_check'], data)

    def get_check_url(self, url_id):
        return self.__execute_query(self.__QUERY['get_check_url'],
                                    (url_id,), fetch='all')

    def get_all_urls(self):
        return self.__execute_query(self.__QUERY['get_urls'], fetch='all')
