import unittest
from project.connection.ConnectionSQLite import ConnectionSQLite
from project.DependencyContainer import DependencyContainer
from project.repository.RepositoryCsv import RepositoryCsv

import sqlite3


class TestConnectionSqlite(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.app = DependencyContainer()
        self.config = self.app.config_conf()  # ConfigurationCONF
        self.sql_connection = ConnectionSQLite(self.config, "CONNECTION_SQLITE_TEST")
        self.csv_repository = RepositoryCsv(self.sql_connection)

    def test_get_connection_sqlite3(self):
        connection = self.sql_connection.get_connection()
        self.assertTrue(isinstance(connection, sqlite3.Connection))


if __name__ == '__main__':
    unittest.main()
