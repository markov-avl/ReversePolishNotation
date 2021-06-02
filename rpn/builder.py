from typing import Callable

from .creator import Creator

from .operations import UnaryOperation, BinaryOperation, Plus, Minus, Multiplication, Division
from .parameters import Fixation, Priority

from .space import Space
from .brackets import OpeningBracket, ClosingBracket


class Builder:
    def __init__(self) -> None:
        self._creator = None

    @property
    def creator(self) -> Creator:
        return self.creator

    @creator.setter
    def creator(self, creator: Creator) -> None:
        self._creator = creator

    def add_plus(self) -> None:
        self._creator.add(str(Plus()), Plus)

    def add_minus(self) -> None:
        self._creator.add(str(Minus()), Minus)

    def add_multiplication(self) -> None:
        self._creator.add(str(Multiplication()), Multiplication)

    def add_division(self) -> None:
        self._creator.add(str(Division()), Division)

    def add_unary_operation(self, symbol: str, function: Callable, fixation: Fixation) -> None:
        UnaryOperation(symbol, function, fixation)
        self._creator.add(symbol, lambda: UnaryOperation(symbol, function, fixation))

    def add_binary_operation(self, symbol: str, function: Callable, priority: Priority) -> None:
        BinaryOperation(symbol, function, priority)
        self._creator.add(symbol, lambda: BinaryOperation(symbol, function, priority))

    def add_space(self) -> None:
        self._creator.add(str(Space()), Space)

    def add_brackets(self) -> None:
        self._creator.add(str(ClosingBracket()), ClosingBracket)
        self._creator.add(str(OpeningBracket()), OpeningBracket)

    def add_standard_operations(self) -> None:
        self.add_plus()
        self.add_minus()
        self.add_multiplication()
        self.add_division()

    def add_all(self) -> None:
        self.add_standard_operations()
        self.add_space()
        self.add_brackets()

    def clear(self) -> None:
        self._creator.clear()
