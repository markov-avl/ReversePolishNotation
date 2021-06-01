from typing import Union

from rpn import RPN, Priority


def power(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    return a ** b


def factorial(a: Union[int, float]) -> int:
    if float(a).is_integer() and int(a) >= 0:
        a = int(a)
        return 1 if a == 0 else factorial(a - 1) * a
    else:
        raise ValueError('Factorial is defined only on non-negative integers')


def reverse_sign(a: Union[int, float]) -> Union[int, float]:
    return a * -1


def main():
    rpn = RPN()
    rpn.add_operation('^', Priority.HIGH, power)
    rpn.add_operation('!', Priority.HIGH, factorial)
    rpn.add_operation('±', Priority.HIGH, reverse_sign)
    rpn.add_all()

    exp = '34 + 3! ^ 2±'
    print(rpn.get_rpn_expression(exp))
    rpn.push_expression(exp)
    print(rpn.solve())


if __name__ == '__main__':
    main()
