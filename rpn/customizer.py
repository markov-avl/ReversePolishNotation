from typing import Callable

from .alphabet import Alphabet

from .operations import UnaryOperation, BinaryOperation, Plus, Minus, Multiplication, Division
from .parameters import Fixation, Priority

from .space import Space
from .brackets import OpeningBracket, ClosingBracket


class Customizer:
    def __init__(self) -> None:
        self._alphabet = None

    @property
    def alphabet(self) -> Alphabet:
        return self.alphabet

    @alphabet.setter
    def alphabet(self, alphabet: Alphabet) -> None:
        self._alphabet = alphabet

    def add_plus(self) -> None:
        self._alphabet.add(str(Plus()), Plus)

    def add_minus(self) -> None:
        self._alphabet.add(str(Minus()), Minus)

    def add_multiplication(self) -> None:
        self._alphabet.add(str(Multiplication()), Multiplication)

    def add_division(self) -> None:
        self._alphabet.add(str(Division()), Division)

    def add_unary_operation(self, symbol: str, function: Callable, fixation: Fixation) -> None:
        UnaryOperation(symbol, function, fixation)
        self._alphabet.add(symbol, lambda: UnaryOperation(symbol, function, fixation))

    def add_binary_operation(self, symbol: str, function: Callable, priority: Priority) -> None:
        BinaryOperation(symbol, function, priority)
        self._alphabet.add(symbol, lambda: BinaryOperation(symbol, function, priority))

    def add_space(self) -> None:
        self._alphabet.add(str(Space()), Space)

    def add_brackets(self) -> None:
        self._alphabet.add(str(ClosingBracket()), ClosingBracket)
        self._alphabet.add(str(OpeningBracket()), OpeningBracket)

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
        self._alphabet.clear()
