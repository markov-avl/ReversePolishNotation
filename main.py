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
    rpn.alphabet = customizer.alphabet = Alphabet()  # или просто customizer.creator = rpn.creator

    customizer.add_all()
    customizer.add_unary_operation('!', factorial, Fixation.POSTFIX)
    customizer.add_unary_operation('↑', inc, Fixation.POSTFIX)
    customizer.add_unary_operation('↓', dec, Fixation.PREFIX)
    customizer.add_binary_operation('^', pow, Priority.HIGH)

    expression = '↓7↑ * 7 ^ (2 + 2)!'

    print(rpn.get_rpn_expression(expression))  # 7 ↓ ↑ 7 * 2 2 + ! ^
    print(rpn.solve_expression(expression))    # 36703368217294125441230211032033660188801


if __name__ == '__main__':
    main()
