import os
from pathlib import Path
from project.repository.RepositoryAbstract import RepositoryAbstract
from project.configuration.ConfigurationAbstract import ConfigurationAbstract

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class ServiceCsv():

    def __init__(self, config: ConfigurationAbstract, repository: RepositoryAbstract):
        self.repository = repository
        self.static_folder = config.get("STATIC", "path")

    def add_Csv(self, url:str, topic: str):
        file_path = "add_csv.sql"
        file_query = os.path.join(BASE_DIR, self.static_folder, file_path)



