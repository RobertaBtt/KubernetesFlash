import unittest
from project.connection.ConnectionSQLite import ConnectionSQLite
from project.DependencyContainer import DependencyContainer
from project.repository.RepositoryCsv import RepositoryCsv
import project.errors
import tests


class TestRepositoryCsv(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.container = DependencyContainer()
        self.config = self.container.config_conf()  # ConfigurationCONF
        self.sql_connection = ConnectionSQLite(self.config, "CONNECTION_SQLITE")
        self.repository_csv = RepositoryCsv(self.sql_connection)

        self.new_url = "http://host/domain/url_world.csv"
        self.sql_read_csv = "select * from CSV limit 1"

        tests.create_table_csv()

    def test_add_csv(self):
        sql_create_csv = f"INSERT INTO CSV(url,topic) VALUES('{self.new_url}','new_topic');"
        self.repository_csv.create(sql_create_csv)

        result = self.repository_csv.read(self.sql_read_csv)

        id_csv, url, topic = result.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(id_csv, 1)
        self.assertEqual(topic, "new_topic")
        self.assertEqual(url, self.new_url)

    def test_delete_csv(self):
        new_id = self.repository_csv.read(f"select id from CSV where url = '{self.new_url}'").fetchone()[0]
        sql_delete_csv = f"DELETE from CSV where id = {new_id}"

        self.repository_csv.delete(sql_delete_csv)

        result = self.repository_csv.read(self.sql_read_csv).fetchone()
        self.assertIsNone(result)

    def test_drop_table(self):
        self.repository_csv.delete("DROP table IF EXISTS CSV")

        with self.assertRaises(self.sql_connection.get_error('OperationalError')):
            self.repository_csv.read(self.sql_read_csv).fetchone()


if __name__ == '__main__':
    unittest.main()
