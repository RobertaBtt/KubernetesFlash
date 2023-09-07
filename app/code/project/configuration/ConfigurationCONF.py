import os
from project.configuration.ConfigurationAbstract import ConfigurationAbstract
from configparser import ConfigParser, NoSectionError, NoOptionError


class ConfigurationCONF(ConfigurationAbstract):
    def __init__(self, config_path: str = '../../config'):
        self.config = None
        self.path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            config_path
        )

    def load(self) -> None:
        self.config = ConfigParser()
        for file in os.listdir(self.path):
            file = os.path.join(self.path, file)

            if os.path.isfile(file):
                self.config.read(file)

    def get(self,section: str, option: str):
        if self.config is None:
            self.load()
        try:
            value = self.config.get(section, option)
            return value
        except NoSectionError:
            raise KeyError (f'Section {section} not found')
        except NoOptionError:
            raise KeyError(f'Option {option} not found')

