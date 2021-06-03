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
    builder = Customizer()
    rpn.creator = builder.creator = Alphabet()  # или просто builder.creator = rpn.creator

    builder.add_all()
    builder.add_unary_operation('!', factorial, Fixation.POSTFIX)
    builder.add_unary_operation('↑', inc, Fixation.POSTFIX)
    builder.add_unary_operation('↓', dec, Fixation.PREFIX)
    builder.add_binary_operation('^', pow, Priority.HIGH)

    expression = '↓7↑ * 7 ^ (2 + 2)!'

    print(rpn.get_rpn_expression(expression))  # 7 ↓ ↑ 7 * 2 2 + ! ^
    print(rpn.solve_expression(expression))    # 36703368217294125441230211032033660188801


if __name__ == '__main__':
    main()
