from abc import ABC

from .symbol import Symbol
from .stack import Stack
from .output import Output


class Digit(Symbol, ABC):
    def __init__(self, digit_symbol: str) -> None:
        super().__init__(digit_symbol)

    def push(self, stack_: Stack, output_: Output, last_symbol: any) -> None:
        if len(output_) > 0 and type(last_symbol) == Digit:
            number = output_.pop_top() * 10 + int(self)
            output_.push(number)
        else:
            output_.push(int(self))

    def __int__(self) -> int:
        return int(self._symbol)
