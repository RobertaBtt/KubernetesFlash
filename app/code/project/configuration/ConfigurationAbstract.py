from abc import ABC, abstractmethod


class ConfigurationAbstract(ABC):
    @abstractmethod
    def get(self, key: str, section: str = None):
        raise NotImplementedError

    @abstractmethod
    def load(self) -> None:
        raise NotImplementedError
