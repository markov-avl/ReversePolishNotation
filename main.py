from rpn import RPN
from rpn import Priority


def power(a: int, b: int) -> int:
    return a ** b


def factorial(a: int) -> int:
    return 1 if a == 0 else factorial(a - 1) * a


def main():
    rpn = RPN()
    rpn.add_operation('^', Priority.HIGH, power)
    rpn.add_operation('!', Priority.HIGH, factorial)
    rpn.add_all()

    exp = '34 + 3! ^ 2'
    print(rpn.get_rpn_expression(exp))
    rpn.push_expression(exp)
    print(rpn.solve())


if __name__ == '__main__':
    main()
