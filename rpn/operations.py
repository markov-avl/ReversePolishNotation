from inspect import signature
from operator import add, sub, mul, itruediv

from .brackets import OpeningBracket
from .symbol import Symbol
from .stack import Stack
from .output import Output
from .priorities import Priority


class Operation(Symbol):
    def __init__(self, operation_symbol: str, priority: Priority, function) -> None:
        super().__init__(operation_symbol)
        self._priority = priority
        self._degree = len(signature(function).parameters)
        if 1 <= self._degree <= 2:
            self._function = function
        else:
            raise ValueError('Constants and operations higher than second degree are not supported =(')

    @property
    def priority(self) -> Priority:
        return self._priority

    @property
    def degree(self) -> int:
        return self._degree

    def _push(self, stack_: Stack, output_: Output) -> None:
        if self._priority == Priority.HIGH and len(stack_) > 0 and stack_.get_top().priority == Priority.HIGH:
            output_.push(stack_.pop_top())
        stack_.push(self)

    # TODO: 4 + (-3) - такое нельзя, а надо бы, чтобы можно было
    def push(self, stack_: Stack, output_: Output, last_symbol: any) -> None:
        if isinstance(last_symbol, Operation) and last_symbol.degree == 2:
            raise SyntaxError('Operation cannot follow after second degree operation')
        elif type(last_symbol) == OpeningBracket:
            raise SyntaxError('Postfix operations cannot follow after opening bracket')
        self._push(stack_, output_)

    def push_out(self, stack_: Stack) -> None:
        args = list()
        for _ in range(self._degree):
            args.append(stack_.pop_top())
        args.reverse()
        stack_.push(self._function(*args))


class Plus(Operation):
    def __init__(self) -> None:
        super().__init__('+', Priority.LOW, add)


class Minus(Operation):
    def __init__(self) -> None:
        super().__init__('-', Priority.LOW, sub)


class Multiplication(Operation):
    def __init__(self) -> None:
        super().__init__('*', Priority.HIGH, mul)


class Division(Operation):
    def __init__(self) -> None:
        super().__init__('/', Priority.HIGH, itruediv)
