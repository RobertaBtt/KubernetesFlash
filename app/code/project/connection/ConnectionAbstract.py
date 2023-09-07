from abc import ABC, abstractmethod


class ConnectionAbstract(ABC):
    @abstractmethod
    def get_connection(self) -> bool:
        raise NotImplementedError
