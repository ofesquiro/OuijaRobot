from .ParseStringStrategy import ParseStringStrategy

class UTF_8(ParseStringStrategy):
    def parse(self, string: bytes) -> str:
        return string.decode('utf-8')

class ISO(ParseStringStrategy):
    def parse(self, string: bytes) -> str:
        return string.decode('iso-8859-1')

class UFT_16(ParseStringStrategy):
    def parse(self, string: bytes) -> str:
        return string.decode('utf-16')

class UFT_32(ParseStringStrategy):
    def parse(self, string: bytes) -> str:
        return string.decode('utf-32')

class Windows_1252(ParseStringStrategy):
    def parse(self, string: bytes) -> str:
        return string.decode('windows-1252')