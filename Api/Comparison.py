from .ParseStringStrategy import ParseStringStrategy
from .Strategies import UTF_8, ISO, UFT_16, UFT_32, Windows_1252
from enum import Enum

class Options(Enum):
    UTF_8 = UTF_8()
    ISO = ISO()
    UFT_16 = UFT_16()
    UFT_32 = UFT_32()
    Windows_1252 = Windows_1252()

    def get_strategy(self) -> ParseStringStrategy:
        return self.value

    def __str__(self) -> str:
        return self.name

strategy: ParseStringStrategy = UTF_8()

def change_strategy(option: Enum) -> None:
    global strategy
    strategy = option.get_strategy()

def parse_string(string: bytes) -> str:
    return strategy.parse(string)

def compare(input: bytes) -> dict[Options, str]:
    options_dict: dict[Options, str] = {}
    for option in Options:
        change_strategy(option)
        try:
            options_dict[option] = parse_string(input)
        except Exception as e:
            print(e)
            continue
    return options_dict