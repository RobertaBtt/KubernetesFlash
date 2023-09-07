import sqlite3
from pathlib import Path
import os
from project.connection.ConnectionAbstract import ConnectionAbstract
from project.configuration.ConfigurationAbstract import ConfigurationAbstract

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ERRORS = {
    'OperationalError': sqlite3.OperationalError
}


class ConnectionSQLite(ConnectionAbstract):

    def __init__(self, config: ConfigurationAbstract, section: str):
        self.db_url = config.get(section, "path")

    def get_connection(self) -> ConnectionAbstract:
        try:
            return sqlite3.connect(os.path.join(str(BASE_DIR) + self.db_url))
        except Exception as e:
            raise e

    def get_error(self, error: str):
        return ERRORS[error] if error in ERRORS else None


