import os
from pathlib import Path
from project.repository.RepositoryAbstract import RepositoryAbstract
from project.configuration.ConfigurationAbstract import ConfigurationAbstract

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def __create_query__(file_query, values_dict:dict ):

    with open(file_query, 'r') as query:
        sql_script = query.read()
        for item,value in values_dict.items():
            sql_script = sql_script.replace(item, str(value))

    return sql_script

class ServiceCsv():

    def __init__(self, config: ConfigurationAbstract, repository: RepositoryAbstract):
        self.repository = repository
        self.static_folder = config.get("STATIC", "path")

    def add_csv(self, values_dict: dict):
        file_path = "add_csv.sql"
        file_query = os.path.join(BASE_DIR, self.static_folder, file_path)

        query = __create_query__(file_query, values_dict)
        self.repository.create(query)

    def get_csv_by_id(self, values_dict: dict):
        file_path = "get_csv_by_id.sql"
        file_query = os.path.join(BASE_DIR, self.static_folder, file_path)
        query = __create_query__(file_query, values_dict)

        result = self.repository.read(query)
        return result.fetchone()

    def get_csv_by_topic(self, values_dict: dict):
        file_path = "get_csv_by_topic.sql"
        file_query = os.path.join(BASE_DIR, self.static_folder, file_path)
        query = __create_query__(file_query, values_dict)
        result = self.repository.read(query)

        csv_records = result.fetchall()
        return csv_records

