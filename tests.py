import unittest

from rpn import RPN, Builder, Creator, Fixation, Priority


class MyTestCase(unittest.TestCase):
    def testSimplestExpression(self):
        rpn = RPN()

        self.assertEqual(rpn.get_rpn_expression('123456789'), '123456789')
        self.assertEqual(rpn.solve_expression('123456789'), 123456789)

        self.assertEqual(rpn.get_rpn_expression('0100'), '100')
        self.assertEqual(rpn.solve_expression('0100'), 100)

        self.assertEqual(rpn.get_rpn_expression('0'), '0')
        self.assertEqual(rpn.solve_expression('0'), 0)

    # Пробел считается символом, который ничего не значит. То есть запись "1 2" распознается в итоге как "12".
    def testSpace(self):
        rpn = RPN()
        builder = Builder()
        builder.creator = rpn.creator
        builder.add_space()

        self.assertEqual(rpn.get_rpn_expression('12345 6789'), '123456789')
        self.assertEqual(rpn.solve_expression('12345 6789'), 123456789)

        self.assertEqual(rpn.get_rpn_expression('0  100'), '100')
        self.assertEqual(rpn.solve_expression('0  100'), 100)

        self.assertEqual(rpn.get_rpn_expression('  0 0  '), '0')
        self.assertEqual(rpn.solve_expression('  0 0  '), 0)


if __name__ == '__main__':
    unittest.main()
