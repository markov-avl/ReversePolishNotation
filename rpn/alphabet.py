from collections import Callable

from .symbol import Symbol
from .digit import Digit


class Alphabet:
    _digits = '0123456789'

    def __init__(self) -> None:
        self._symbols = dict()

    def _check_symbol(self, symbol: str) -> None:
        if symbol in self._digits:
            raise ValueError('Cannot override digit')

    def add(self, symbol: str, constructor: Callable) -> None:
        self._check_symbol(symbol)
        self._symbols[symbol] = constructor

    def clear(self) -> None:
        self._symbols.clear()

    def create(self, symbol: str) -> Symbol:
        if symbol in self._digits:
            return Digit(symbol)
        elif symbol in self._symbols:
            return self._symbols[symbol]()
        raise SyntaxError(f'Got invalid symbol: <{symbol}>')
