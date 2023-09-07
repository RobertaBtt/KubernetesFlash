from abc import abstractmethod, ABC


class RepositoryAbstract(ABC):

    @abstractmethod
    def create(self, query: str):
        raise NotImplementedError

    @abstractmethod
    def check_table(self, query: str):
        raise NotImplementedError

    @abstractmethod
    def read(self, query: str):
        raise NotImplementedError

    @abstractmethod
    def read_with_headers(self, query: str):
        raise NotImplementedError

    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def delete(self, query: str):
        raise NotImplementedError

