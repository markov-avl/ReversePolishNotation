from .symbol import Symbol
from .stack import Stack
from .output import Output


class OpeningBracket(Symbol):
    def __init__(self) -> None:
        super().__init__('(')

    def push(self, stack: Stack, output: Output, last_symbol: any) -> None:
        stack.push(self)


class ClosingBracket(Symbol):
    def __init__(self) -> None:
        super().__init__(')')

    def push(self, stack: Stack, output: Output, last_symbol: any) -> None:
        for _ in range(len(stack)):
            if isinstance(stack.top(), OpeningBracket):
                stack.pop()
                break
            output.push(stack.pop())
        else:
            raise SyntaxError('Too many closing brackets')
