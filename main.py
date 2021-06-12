from typing import Union
from operator import pow
from math import factorial

from rpn import RPN, Customizer, Alphabet, Fixation, Priority


def inc(a: Union[int, float, complex]) -> Union[int, float, complex]:
    return a + 1


def dec(a: Union[int, float, complex]) -> Union[int, float, complex]:
    return a - 1


def main():
    rpn = RPN()
    customizer = Customizer()
    rpn.alphabet = customizer.alphabet = Alphabet()  # или просто customizer.alphabet = rpn.alphabet

    customizer.add_all()
    customizer.add_unary_operation('!', factorial, Fixation.POSTFIX)
    customizer.add_unary_operation('↑', inc, Fixation.POSTFIX)
    customizer.add_unary_operation('↓', dec, Fixation.PREFIX)
    customizer.add_binary_operation('^', pow, Priority.HIGHEST)

    expression = '↓7↑ * 7 ^ (2 + 2)!'          # = 7 * 7 ^ 24 = 7 ^ 25

    print(rpn.get_rpn_expression(expression))  # 7 ↓ ↑ 7 2 2 + ! ^ *
    print(rpn.solve_expression(expression))    # 1341068619663964900807


if __name__ == '__main__':
    main()
