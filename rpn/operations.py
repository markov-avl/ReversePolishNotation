from abc import ABC, abstractmethod
from inspect import signature
from operator import add, sub, mul, itruediv
from typing import Callable, Union

from .brackets import OpeningBracket, ClosingBracket
from .symbol import Symbol
from .stack import Stack
from .output import Output
from .parameters import Fixation, Priority


def reverse_sign(a: Union[int, float, complex]) -> Union[int, float, complex]:
    return -a


class Operation(Symbol, ABC):
    def __init__(self, symbol: str, function: Callable) -> None:
        super().__init__(symbol)
        self._function = function
        self._degree = len(signature(function).parameters)

    @property
    def degree(self) -> int:
        return self._degree

    @abstractmethod
    def push(self, stack: Stack, output: Output, last_symbol: any) -> None:
        pass

    @abstractmethod
    def _push(self, stack: Stack, output: Output) -> None:
        pass

    def push_out(self, stack: Stack) -> None:
        args = list()
        for _ in range(self._degree):
            args.append(stack.pop())
        args.reverse()
        stack.push(self._function(*args))


class UnaryOperation(Operation):
    def __init__(self, symbol: str, function: Callable, fixation: Fixation) -> None:
        super().__init__(symbol, function)
        if self._degree != 1:
            raise ValueError('Is not a unary operation')
        self._fixation = fixation

    @property
    def fixation(self) -> Fixation:
        return self._fixation

    def push(self, stack: Stack, output: Output, last_symbol: any) -> None:
        if self._fixation:
            if isinstance(last_symbol, UnaryOperation) and not last_symbol.fixation \
                    or isinstance(last_symbol, BinaryOperation) or isinstance(last_symbol, OpeningBracket):
                raise SyntaxError('Postfix unary operation cannot follow after other operation and opening bracket')
        else:
            if isinstance(last_symbol, ClosingBracket):
                raise SyntaxError('Prefix unary operation cannot follow after another prefix unary operation '
                                  'and closing bracket')
        self._push(stack, output)

    def _push(self, stack: Stack, output: Output) -> None:
        if self._fixation:
            output.push(self)
            if len(stack) and isinstance(stack.top(), BinaryOperation) and stack.top().priority:
                output.push(stack.pop())
        else:
            stack.push(self)


class BinaryOperation(Operation):
    def __init__(self, symbol: str, function: Callable, priority: Priority) -> None:
        super().__init__(symbol, function)
        if self._degree != 2:
            raise ValueError('Is not a binary operation')
        self._priority = priority

    @property
    def priority(self) -> Priority:
        return self._priority

    def push(self, stack: Stack, output: Output, last_symbol: any) -> None:
        if isinstance(last_symbol, UnaryOperation) and not last_symbol.fixation or \
                isinstance(last_symbol, BinaryOperation) or isinstance(last_symbol, OpeningBracket):
            raise SyntaxError('Binary operation cannot follow after prefix unary operation, another binary operation'
                              'and opening bracket')
        self._push(stack, output)

    def _push(self, stack: Stack, output: Output) -> None:
        while isinstance(stack.top(), UnaryOperation) and not stack.top().fixation or \
                isinstance(stack.top(), BinaryOperation) and stack.top().priority >= self._priority:
            output.push(stack.pop())
        stack.push(self)


class Plus(BinaryOperation):
    def __init__(self) -> None:
        super().__init__('+', add, Priority.LOW)


class Minus(BinaryOperation):
    def __init__(self) -> None:
        super().__init__('-', sub, Priority.LOW)

    def push(self, stack: Stack, output: Output, last_symbol: any) -> None:
        if last_symbol is None or isinstance(last_symbol, OpeningBracket):
            unary_minus = UnaryOperation('-', reverse_sign, Fixation.PREFIX)
            unary_minus.push(stack, output, last_symbol)
        else:
            super().push(stack, output, last_symbol)


class Multiplication(BinaryOperation):
    def __init__(self) -> None:
        super().__init__('*', mul, Priority.HIGH)


class Division(BinaryOperation):
    def __init__(self) -> None:
        super().__init__('/', itruediv, Priority.HIGH)
