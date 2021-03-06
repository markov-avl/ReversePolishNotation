from typing import Union

from .operations import UnaryOperation, BinaryOperation
from .space import Space
from .brackets import OpeningBracket

from .stack import Stack
from .output import Output
from .alphabet import Alphabet


class RPN:
    def __init__(self) -> None:
        self._stack = Stack()
        self._output = Output()
        self._creator = Alphabet()
        self._last_symbol = None

    @property
    def alphabet(self) -> Alphabet:
        return self._creator

    @alphabet.setter
    def alphabet(self, creator: Alphabet) -> None:
        self._creator = creator

    def _clear(self) -> None:
        self._stack.clear()
        self._output.clear()
        self._last_symbol = None

    def _push_from_stack_to_output(self) -> None:
        for _ in range(len(self._stack)):
            if isinstance(self._stack.top(), OpeningBracket):
                raise SyntaxError('Too many opening brackets')
            self._output.push(self._stack.pop())

    def push_expression(self, expression: str) -> None:
        self._clear()
        for symbol in expression:
            valid_symbol = self._creator.create(symbol)
            valid_symbol.push(self._stack, self._output, self._last_symbol)
            if not isinstance(valid_symbol, Space):
                self._last_symbol = valid_symbol
        if isinstance(self._last_symbol, UnaryOperation) and not self._last_symbol.fixation or \
                isinstance(self._last_symbol, BinaryOperation) or isinstance(self._last_symbol, OpeningBracket):
            raise SyntaxError(f'Invalid ending of the expression: <{self._last_symbol}>')
        self._push_from_stack_to_output()

    def solve(self) -> Union[int, float, complex]:
        for item in self._output:
            if isinstance(item, int):
                self._stack.push(item)
            else:
                item.push_out(self._stack)
        if self._stack.top() is not None and not isinstance(self._stack.top(), complex) and \
                float(self._stack.top()).is_integer():
            return int(self._stack.pop())
        return self._stack.pop() if len(self._stack) else None

    def get_rpn_expression(self, expression: str) -> str:
        self.push_expression(expression)
        return ' '.join(map(str, self._output))

    def solve_expression(self, expression: str) -> Union[int, float, complex]:
        self.push_expression(expression)
        return self.solve()
