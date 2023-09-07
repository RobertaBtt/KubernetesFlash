from project.connection.ConnectionSQLite import ConnectionSQLite
from project.DependencyContainer import DependencyContainer
from project.repository.RepositoryCsv import RepositoryCsv


@staticmethod
def create_table_csv():
    container = DependencyContainer()
    config = container.config_conf()  # ConfigurationCONF
    sql_connection = ConnectionSQLite(config, "CONNECTION_SQLITE")

    repository_csv = RepositoryCsv(sql_connection)

    repository_csv.create("CREATE TABLE IF NOT EXISTS CSV (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                          "url CHAR NOT NULL UNIQUE,topic CHAR NOT NULL);")