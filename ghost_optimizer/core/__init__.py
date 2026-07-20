from abc import ABC, abstractmethod

class BaseTweak(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def apply(self) -> bool:
        pass

    @abstractmethod
    def restore(self) -> bool:
        pass
