from abc import ABC, abstractmethod
class ParseStringStrategy(ABC):
    @abstractmethod
    def parse(self, string) -> str:
        pass