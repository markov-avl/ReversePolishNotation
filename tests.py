import unittest
from typing import Union
from operator import add, sub, pow
from math import factorial

from rpn import RPN, Customizer, Alphabet, Fixation, Priority


class RPNTestCase(unittest.TestCase):
    _rpn = RPN()
    _builder = Customizer()
    
    @staticmethod
    def inc(a: Union[int, float, complex]) -> Union[int, float, complex]:
        return a + 1

    @staticmethod
    def dec(a: Union[int, float, complex]) -> Union[int, float, complex]:
        return a - 1

    @staticmethod
    def constant() -> int:
        return 0

    @staticmethod
    def multiple_operation(*args, **kwargs):
        return sum(args, kwargs.values())

    # Самым простым выражением считается просто число. Экземпляры класса RPN по умолчанию умеют решать такие выражения.
    def testSimplestExpression(self) -> None:
        self.assertEqual(self._rpn.get_rpn_expression('123456789'), '123456789')
        self.assertEqual(self._rpn.solve_expression('123456789'), 123456789)
        self.assertEqual(self._rpn.get_rpn_expression('0100'), '100')
        self.assertEqual(self._rpn.solve_expression('0100'), 100)
        self.assertEqual(self._rpn.get_rpn_expression('0'), '0')
        self.assertEqual(self._rpn.solve_expression('0'), 0)

    # Пробел считается символом, который ничего не значит. Например, запись "1 2" распознается в итоге как "12"
    def testSpace(self) -> None:
        self._rpn.creator = self._builder.creator = Alphabet()
        self._builder.add_space()

        self.assertEqual(self._rpn.get_rpn_expression('12345 6789'), '123456789')
        self.assertEqual(self._rpn.solve(), 123456789)
        self.assertEqual(self._rpn.get_rpn_expression('0  100'), '100')
        self.assertEqual(self._rpn.solve(), 100)
        self.assertEqual(self._rpn.get_rpn_expression('  0 0  '), '0')
        self.assertEqual(self._rpn.solve(), 0)

    def testStandardOperations(self) -> None:
        self._rpn.creator = self._builder.creator = Alphabet()
        self._builder.add_space()
        self._builder.add_standard_operations()

        self.assertEqual(self._rpn.get_rpn_expression('1 + 2 - 3 * 4 / 5'), '1 2 + 3 4 * 5 / -')
        self.assertAlmostEqual(self._rpn.solve(), 0.6)
        self.assertEqual(self._rpn.get_rpn_expression('-4 - 32 * 2 + 9 / 3 - 1'), '4 - 32 2 * - 9 3 / + 1 -')
        self.assertAlmostEqual(self._rpn.solve(), -66)
        self.assertEqual(self._rpn.get_rpn_expression('-3 * 8 + 99 / 1'), '3 - 8 * 99 1 / +')
        self.assertAlmostEqual(self._rpn.solve(), 75)

    def testBrackets(self) -> None:
        self._rpn.creator = self._builder.creator = Alphabet()
        self._builder.add_space()
        self._builder.add_standard_operations()
        self._builder.add_brackets()
        
        self.assertEqual(self._rpn.get_rpn_expression('(1 + 2) - 3 * (4 / 4)'), '1 2 + 3 4 4 / * -')
        self.assertAlmostEqual(self._rpn.solve(), 0)
        self.assertEqual(self._rpn.get_rpn_expression('-4 - 32 * (-2) + (9) / (4 - 1)'), '4 - 32 2 - * - 9 4 1 - / +')
        self.assertAlmostEqual(self._rpn.solve(), 63)
        self.assertEqual(self._rpn.get_rpn_expression('-3 * (8 + 99) / 1'), '3 - 8 99 + * 1 /')
        self.assertAlmostEqual(self._rpn.solve(), -321)
        self.assertEqual(self._rpn.get_rpn_expression('(1 / 2) * () (1 / 4)'), '1 2 / 1 4 / *')
        self.assertAlmostEqual(self._rpn.solve(), 0.125)

    def testSelfWrittenOperations(self) -> None:
        self._rpn.creator = self._builder.creator = Alphabet()
        self._builder.add_all()
        self._builder.add_unary_operation('!', factorial, Fixation.POSTFIX)
        self._builder.add_unary_operation('↑', self.inc, Fixation.POSTFIX)
        self._builder.add_unary_operation('↓', self.dec, Fixation.PREFIX)
        self._builder.add_binary_operation('^', pow, Priority.HIGH)

        self.assertEqual(self._rpn.get_rpn_expression('↓↓1↑↑↑↑ + 7 ^ 2 + 4!'), '1 ↓ ↑ ↑ ↑ ↑ ↓ 7 2 ^ + 4 ! +')
        self.assertAlmostEqual(self._rpn.solve(), 76)
        self.assertEqual(self._rpn.get_rpn_expression('-1↑! + ↓7 ^ (2 * (1 + 1)!)'), '1 - ↑ ! 7 ↓ 2 1 1 + ! * ^ +')
        self.assertAlmostEqual(self._rpn.solve(), 1297)
        self.assertEqual(self._rpn.get_rpn_expression('-4 ^ (1 / 2)'), '4 - 1 2 / ^')
        self.assertEqual(self._rpn.solve().imag, 2)  # Проверяем лишь мнимую часть числа, этого хватит.

    # Переопределение уже существующей операции не является ошибкой, поэтому с этим стоит быть осторожно.
    def testOperationOverride(self) -> None:
        self._rpn.creator = self._builder.creator = Alphabet()
        self._builder.add_all()
        self._builder.add_binary_operation('+', sub, Priority.LOW)
        self._builder.add_binary_operation('-', add, Priority.LOW)

        self.assertEqual(self._rpn.get_rpn_expression('100 + 50 + 25'), '100 50 + 25 +')
        self.assertAlmostEqual(self._rpn.solve(), 25)
        self.assertEqual(self._rpn.get_rpn_expression('100 - 50 - 25'), '100 50 - 25 -')
        self.assertAlmostEqual(self._rpn.solve(), 175)
        self.assertEqual(self._rpn.get_rpn_expression('100 * 2 + 50 * 2 - 25 * 2'), '100 2 * 50 2 * + 25 2 * -')
        self.assertAlmostEqual(self._rpn.solve(), 150)

        self._builder.add_binary_operation(' ', add, Priority.LOW)

        self.assertEqual(self._rpn.get_rpn_expression('4 89 29 1 8 3'), '4 89 + 29 + 1 + 8 + 3 +'.replace('+', ' '))
        self.assertAlmostEqual(self._rpn.solve(), 134)

    def testEmptyExpression(self) -> None:
        self._rpn.creator = self._builder.creator = Alphabet()
        self._builder.add_all()

        self.assertEqual(self._rpn.get_rpn_expression(''), '')
        self.assertEqual(self._rpn.solve(), None)
        self.assertEqual(self._rpn.get_rpn_expression('()'), '')
        self.assertEqual(self._rpn.solve(), None)
        self.assertEqual(self._rpn.get_rpn_expression('(())'), '')
        self.assertEqual(self._rpn.solve(), None)
        self.assertEqual(self._rpn.get_rpn_expression('( )'), '')
        self.assertEqual(self._rpn.solve(), None)

    def testSyntaxError(self) -> None:
        # Найдены неизвестные символы:
        self._rpn.creator = Alphabet()
        self.assertRaises(SyntaxError, self._rpn.push_expression, '1 2')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '1+2')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '1_2')

        # Нарушение языка выражений:
        self._builder.creator = self._rpn.creator
        self._builder.add_all()
        self._builder.add_unary_operation('↑', self.inc, Fixation.POSTFIX)
        self._builder.add_unary_operation('↓', self.dec, Fixation.PREFIX)
        self.assertRaises(SyntaxError, self._rpn.push_expression, '+')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '*')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '(')
        self.assertRaises(SyntaxError, self._rpn.push_expression, ')')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '1 +')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '1 *')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '1 (')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '1 )')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '1 + -2')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '1 + + 2')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '1 * * 2')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '+1')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '*1')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '1 + (-2')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '1 + ((-2)')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '1) + 2')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '(1)) + 2')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '1↓')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '↑1')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '↓↓')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '↑↑')

    def testValueError(self) -> None:
        self._rpn.creator = self._builder.creator = Alphabet()
        self._builder.add_all()

        # Добавление операции с недопустимым символом:
        self.assertRaises(ValueError, self._builder.add_binary_operation, '', add, Priority.LOW)
        self.assertRaises(ValueError, self._builder.add_binary_operation, '0', add, Priority.LOW)
        self.assertRaises(ValueError, self._builder.add_binary_operation, 'add', add, Priority.LOW)

        # Нарушение соглашения об унарности/бинарности новой операции:
        self.assertRaises(ValueError, self._builder.add_unary_operation, 'o', self.constant, Fixation.PREFIX)
        self.assertRaises(ValueError, self._builder.add_unary_operation, '+', self.multiple_operation, Fixation.PREFIX)
        self.assertRaises(ValueError, self._builder.add_binary_operation, 'o', self.constant, Priority.HIGH)
        self.assertRaises(ValueError, self._builder.add_binary_operation, '+', self.multiple_operation, Priority.HIGH)


if __name__ == '__main__':
    unittest.main()
