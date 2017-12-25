from abc import ABC, abstractmethod


class AbstractCleaningAlgorithm(ABC):

    @abstractmethod
    def update(self, env):
        pass


class BaseCleaningAlgorithm(AbstractCleaningAlgorithm):

    def update(self, env):
        pass
