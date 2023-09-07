from project.repository.RepositoryAbstract import RepositoryAbstract
from project.connection.ConnectionAbstract import ConnectionAbstract


class RepositoryCsv(RepositoryAbstract):

    def __init__(self, connection: ConnectionAbstract):
        self.sql = connection

    def create(self, query: str):
        with self.sql.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

    def read_with_headers(self, query: str):
        with self.sql.get_connection() as connection:
            cursor = connection.cursor()
            result = cursor.execute(query).fetchall()
            headers = list(map(lambda attr: attr[0], cursor.description))
            results = [{header: row[i] for i, header in enumerate(headers)} for row in result]

        return results

    def read(self, query: str):
        with self.sql.get_connection() as connection:
            cursor = connection.cursor()
            result = cursor.execute(query)

        return result

    def update(self):
        pass

    def delete(self, query: str):
        with self.sql.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()

    def check_table(self, query: str):
        pass