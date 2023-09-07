from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton
from project.connection.ConnectionSQLite import ConnectionSQLite

from project.configuration.ConfigurationCONF import ConfigurationCONF
from project.connection.ConnectionSQLite import ConnectionSQLite
from project.service.ServiceCsv import ServiceCsv

class DependencyContainer(DeclarativeContainer):

    config_conf = Singleton(ConfigurationCONF)

    connection = Singleton(ConnectionSQLite, config_conf, "CONNECTION_SQLITE")

    service_csv = Singleton(ConnectionSQLite, config_conf)


