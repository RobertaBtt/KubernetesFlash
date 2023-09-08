import unittest
from project.connection.ConnectionSQLite import ConnectionSQLite
from project.DependencyContainer import DependencyContainer
from project.repository.RepositoryCsv import RepositoryCsv
from project.service.ServiceCsv import ServiceCsv
import tests

class TestServiceCsv(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.container = DependencyContainer()
        self.config = self.container.config_conf()  # ConfigurationCONF
        self.sql_connection = ConnectionSQLite(self.config, "CONNECTION_SQLITE")

        self.repository_csv = RepositoryCsv(self.sql_connection)
        self.service_csv = ServiceCsv(self.config, self.repository_csv)

        tests.create_table_csv()


    def test_add_csv_and_get_by_topic(self):
        topic_1 = 'environment'
        url_1 = "https://host/wildfires.csv"
        url_2 = "https://host/georadar_stations.csv"

        self.service_csv.add_csv({'%URL%': url_1, '%TOPIC%': topic_1})
        self.service_csv.add_csv({'%URL%': url_2, '%TOPIC%': topic_1})

        res = self.service_csv.get_csv_by_topic({'%TOPIC%': topic_1})

        # [(1, 'https://host/wildfires.csv', 'environment')]
        # id, url, topic

        self.assertIsNotNone(res)
        self.assertEqual(res[0][2], topic_1)
        self.assertEqual(res[1][2], topic_1)

        self.assertEqual(res[1][1], url_2)

    def test_get_csv_by_id(self):
        record = self.service_csv.get_csv_by_id({'%ID%': 1})

        self.assertIsNotNone(record)

        self.assertEqual(record[0], 1)
        self.assertEqual(record[1], "https://host/wildfires.csv")
        self.assertEqual(record[2], "environment")

    def test_get_csv_by_id_not_exist(self):
        record = self.service_csv.get_csv_by_id({'%ID%': 9999})
        self.assertIsNone(record)


    def test_get_csv_by_url(self):
        topic = 'software'
        url = "https://github.com/gist/test.csv"

        self.service_csv.add_csv({'%URL%': url, '%TOPIC%': topic})

        record = self.service_csv.get_csv_by_url({'%URL%': url})

        self.assertIsNotNone(record)

        self.assertEqual(record[1], url)
        self.assertEqual(record[2], topic)

        self.repository_csv.delete("DROP table IF EXISTS CSV")






