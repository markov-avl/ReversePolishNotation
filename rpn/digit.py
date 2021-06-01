from abc import ABC

from .symbol import Symbol
from .stack import Stack
from .output import Output


class Digit(Symbol, ABC):
    def __init__(self, digit_symbol: str) -> None:
        super().__init__(digit_symbol)

    def push(self, stack: Stack, output: Output, last_symbol: any) -> None:
        if len(output) > 0 and type(last_symbol) == Digit:
            number = output.pop_top() * 10 + int(self)
            output.push(number)
        else:
            output.push(int(self))

    def __int__(self) -> int:
        return int(self._symbol)
