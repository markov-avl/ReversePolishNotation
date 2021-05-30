from .symbol import Symbol


class OpeningBracket(Symbol):
    def __init__(self) -> None:
        super().__init__('(')


class ClosingBracket(Symbol):
    def __init__(self) -> None:
        super().__init__(')')
