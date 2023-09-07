"""
GIVEN a Flask application configured for testing
WHEN the '/' page is requested (GET)
THEN response is valid
THEN output is valid
"""

import json
import tests
from project.connection.ConnectionSQLite import ConnectionSQLite
from project.DependencyContainer import DependencyContainer
from project.repository.RepositoryCsv import RepositoryCsv
from project.service.ServiceCsv import ServiceCsv
import project.errors as er
import pytest


container = DependencyContainer()
config = container.config_conf()  # ConfigurationCONF
sql_connection = ConnectionSQLite(config, "CONNECTION_SQLITE")

repository_csv = RepositoryCsv(sql_connection)
service_csv = ServiceCsv(config, repository_csv)

tests.create_table_csv()


def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"App Works!" in response.data


def test_post_csv(test_client):
    csv_url = "https://vincentarelbundock.github.io/Rdatasets/csv/stevedata/quartets.csv"
    topic = "economy"

    dict_data = {'url': csv_url,
                 'topic': topic
                 }
    response = test_client.post("/csv", data=json.dumps(dict_data), content_type='text/json; charset=utf-8')

    assert response.status_code == 200


def test_csv_by_topic(test_client):
    topic_test = "economy"
    response = test_client.get(f'/topic/{topic_test}/csv/')
    assert response.status_code == 200
    assert b"topic" in response.data


def test_csv_by_id(test_client):
    csv_id = "1"
    response = test_client.get(f'/csv/{csv_id}/')
    assert response.status_code == 200
    assert b'"rownames,x,y,group"' in response.data


def test_csv_by_id_not_exist(test_client):
    csv_id = "9999"

    response = test_client.get(f'/csv/{csv_id}/')

    assert response.status_code == 404


def test_drop_table(test_client):
    repository_csv.delete("DROP table IF EXISTS CSV")


