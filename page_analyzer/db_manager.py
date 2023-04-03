class DBManager:
    def __init__(self, conn):
        self.conn = conn

    def create_table(self):
        with open("database.sql", "r") as file:
            create_tables_query = file.read()

        with self.conn.cursor() as cursor:
            cursor.execute(create_tables_query)
            self.conn.commit()


    def get_url_by_id(self, url_id):
        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, created_at \
                    FROM urls WHERE id = %s", (url_id,)
            )
            url = cursor.fetchone()
            return url

    def get_all_urls(self):
        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, created_at FROM urls \
                    ORDER BY created_at DESC"
            )
            all_urls = cursor.fetchall()
        return all_urls

    def add_url(self, url):
        url_id = None

        with self.conn.cursor() as cursor:
            cursor.execute("SELECT id FROM urls WHERE name = %s", (url,))
            result = cursor.fetchone()

            if result:
                url_id = result[0]
            else:
                cursor.execute(
                    "INSERT INTO urls (name, created_at) \
                        VALUES (%s, NOW()) RETURNING id", (url,)
                )
                url_id = cursor.fetchone()[0]
                self.conn.commit()

        return url_id, bool(result)
