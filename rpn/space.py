from .symbol import Symbol
from .stack import Stack
from .output import Output


class Space(Symbol):
    def __init__(self) -> None:
        super().__init__(' ')

    def push(self, stack: Stack, output: Output, last_symbol: any) -> None:
        pass
