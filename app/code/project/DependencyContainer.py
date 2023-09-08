from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton
from project.configuration.ConfigurationCONF import ConfigurationCONF
from project.connection.ConnectionSQLite import ConnectionSQLite
from project.service.ServiceCsv import ServiceCsv
from project.repository.RepositoryCsv import RepositoryCsv
from project.downloader import get_downloader


class DependencyContainer(DeclarativeContainer):
    config_conf = Singleton(ConfigurationCONF)

    connection = Singleton(ConnectionSQLite, config_conf, "CONNECTION_SQLITE")

    repository = Singleton(RepositoryCsv, connection)

    service_csv = Singleton(ServiceCsv, config_conf, repository)

    downloader_config_method = config_conf().get("DOWNLOADER", "strategy")

    downloader = Singleton(get_downloader(downloader_config_method))  # a function

