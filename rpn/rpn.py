from typing import Union

from .priorities import Priority
from .space import Space
from .digit import Digit
from .operations import Operation, Plus, Minus, Multiplication, Division
from .brackets import OpeningBracket, ClosingBracket

from .stack import Stack
from .output import Output


class RPN:
    def __init__(self) -> None:
        self._stack = Stack()
        self._output = Output()
        self._symbols = dict()
        self.__digits = '0123456789'
        self.__last_symbol = None

    def _clear(self) -> None:
        self._stack.clear()
        self._output.clear()
        self.__last_symbol = None

    def add_space(self) -> None:
        self._symbols[str(Space())] = Space

    def add_plus(self) -> None:
        self._symbols[str(Plus())] = Plus

    def add_minus(self) -> None:
        self._symbols[str(Minus())] = Minus

    def add_multiplication(self) -> None:
        self._symbols[str(Multiplication())] = Multiplication

    def add_division(self) -> None:
        self._symbols[str(Division())] = Division

    def add_operation(self, symbol: str, priority: Priority, function) -> None:
        Operation(symbol, priority, function)
        self._symbols[symbol] = lambda: Operation(symbol, priority, function)

    def add_standard_operations(self) -> None:
        self.add_plus()
        self.add_minus()
        self.add_multiplication()
        self.add_division()

    def add_brackets(self) -> None:
        self._symbols[str(OpeningBracket())] = OpeningBracket
        self._symbols[str(ClosingBracket())] = ClosingBracket

    def add_all(self) -> None:
        self.add_space()
        self.add_standard_operations()
        self.add_brackets()

    def clear_symbols(self) -> None:
        self._symbols.clear()

    # TODO: до сих пор не работают скобки
    def push_expression(self, expression: str) -> None:
        self._clear()
        for symbol in expression:
            # TODO: лучше добавить фабрику
            if symbol in self._symbols:
                valid_symbol = self._symbols[symbol]()
            elif symbol in self.__digits:
                valid_symbol = Digit(symbol)
            else:
                raise SyntaxError(f'Found invalid symbol: <{symbol}>')
            valid_symbol.push(self._stack, self._output, self.__last_symbol)
            if type(valid_symbol) != Space:
                self.__last_symbol = valid_symbol
        for _ in range(len(self._stack)):
            self._output.push(self._stack.pop_top())

    def solve(self) -> Union[int, float]:
        for item in self._output:
            if isinstance(item, int):
                self._stack.push(item)
            else:
                item.push_out(self._stack)
        return self._stack.pop_top()

    def get_rpn_expression(self, expression: str) -> str:
        self.push_expression(expression)
        return ' '.join(map(str, self._output))

    def solve_rpn_expression(self, rpn_expression: str) -> Union[int, float]:
        pass

    def solve_expression(self, expression: str) -> Union[int, float]:
        self.push_expression(expression)
        return self.solve()
