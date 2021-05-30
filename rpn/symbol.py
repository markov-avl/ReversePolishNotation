from abc import abstractmethod

from .stack import Stack
from .output import Output


class Symbol:
    def __init__(self, symbol: str) -> None:
        if len(symbol) == 1:
            self._symbol = symbol
        else:
            raise ValueError('A symbol must be represented by only one character')

    @abstractmethod
    def push(self, stack_: Stack, output_: Output, last_symbol: any) -> None:
        pass

    def __str__(self) -> str:
        return self._symbol
