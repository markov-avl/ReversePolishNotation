from typing import Union
from operator import pow
from math import factorial

from rpn import RPN, Builder, Fixation, Priority


def inc(a: Union[int, float, complex]) -> Union[int, float, complex]:
    return a + 1


def dec(a: Union[int, float, complex]) -> Union[int, float, complex]:
    return a - 1


def add(a, b):
    return a + b


def main():
    rpn = RPN()
    builder = Builder()
    builder.creator = rpn.creator

    builder.add_space()
    builder.add_standard_operations()

    # builder.add_binary_operation(' ', add, Priority.LOW)

    # builder.add_unary_operation('!', factorial, Fixation.POSTFIX)
    # builder.add_unary_operation('↑', inc, Fixation.POSTFIX)
    # builder.add_unary_operation('↓', dec, Fixation.PREFIX)
    # builder.add_binary_operation('^', pow, Priority.HIGH)
    # builder.add_all()

    # expression = '↓1↑↑↑ + 7 ^ 2 + 4!'
    expression = '1 + 4 + 1 * 33'  # в таком случае тогда пробел будет работать как конкатенация D:

    print(rpn.get_rpn_expression(expression))
    rpn.push_expression(expression)
    print(rpn.solve())  # -> 14033


if __name__ == '__main__':
    main()
