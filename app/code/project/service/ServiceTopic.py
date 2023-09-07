from project.repository.RepositoryAbstract import RepositoryAbstract
from project.configuration.ConfigurationAbstract import ConfigurationAbstract


class ServiceTopic():

    def __init__(self, config: ConfigurationAbstract, repository: RepositoryAbstract):
        self.repository = repository
        self.static_folder = config.get("STATIC", "path")