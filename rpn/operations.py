from inspect import signature
from operator import add, sub, mul, itruediv
from typing import Callable

from .brackets import OpeningBracket
from .symbol import Symbol
from .stack import Stack
from .output import Output
from .priorities import Priority


class Operation(Symbol):
    def __init__(self, symbol: str, priority: Priority, function: Callable) -> None:
        super().__init__(symbol)
        self._priority = priority
        self._degree = len(signature(function).parameters)
        if 1 <= self._degree <= 2:
            self._function = function
        else:
            raise ValueError('Only unary and binary operations are supported =(')

    @property
    def priority(self) -> Priority:
        return self._priority

    @property
    def degree(self) -> int:
        return self._degree

    def _push(self, stack: Stack, output: Output) -> None:
        if self._priority:
            if self._degree == 1:
                output.push(self)
            if len(stack) > 0 and isinstance(stack.top(), Operation) and stack.top().priority:
                output.push(stack.pop_top())
            if self._degree == 2:
                stack.push(self)
        else:
            if len(stack) > 0 and isinstance(stack.top(), Operation) and stack.top().priority:
                output.push(stack.pop_top())
            stack.push(self)

    # TODO: 4 + (-3) - такое нельзя, а надо бы, чтобы можно было
    def push(self, stack: Stack, output: Output, last_symbol: any) -> None:
        if isinstance(last_symbol, Operation) and last_symbol.degree == 2:
            raise SyntaxError('Operation cannot follow after second degree operation')
        elif type(last_symbol) == OpeningBracket:
            raise SyntaxError('Postfix operations cannot follow after opening bracket')
        self._push(stack, output)

    def push_out(self, stack: Stack) -> None:
        args = list()
        for _ in range(self._degree):
            args.append(stack.pop_top())
        args.reverse()
        stack.push(self._function(*args))


class Plus(Operation):
    def __init__(self) -> None:
        super().__init__('+', Priority.LOW, add)


class Minus(Operation):
    def __init__(self) -> None:
        super().__init__('-', Priority.LOW, sub)

    def push(self, stack: Stack, output: Output, last_symbol: any) -> None:
        if len(stack) + len(output) == 0 or isinstance(last_symbol, OpeningBracket):
            output.push(0)
            self._priority = Priority.HIGH
            self._push(stack, output)
        else:
            super().push(stack, output, last_symbol)


class Multiplication(Operation):
    def __init__(self) -> None:
        super().__init__('*', Priority.HIGH, mul)


class Division(Operation):
    def __init__(self) -> None:
        super().__init__('/', Priority.HIGH, itruediv)
