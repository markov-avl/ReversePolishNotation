import unittest
from typing import Union
from operator import add, sub, pow
from math import factorial

from rpn import RPN, Customizer, Alphabet, Fixation, Priority


class RPNTestCase(unittest.TestCase):
    _rpn = RPN()
    _customizer = Customizer()
    
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
    def ternary_operation(a: bool, b: Union[int, float, complex],
                          c: Union[int, float, complex]) -> Union[int, float, complex]:
        return b if a else c

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
        self._rpn.alphabet = self._customizer.alphabet = Alphabet()
        self._customizer.add_space()

        self.assertEqual(self._rpn.get_rpn_expression('12345 6789'), '123456789')
        self.assertEqual(self._rpn.solve(), 123456789)
        self.assertEqual(self._rpn.get_rpn_expression('0  100'), '100')
        self.assertEqual(self._rpn.solve(), 100)
        self.assertEqual(self._rpn.get_rpn_expression('  0 0  '), '0')
        self.assertEqual(self._rpn.solve(), 0)

    def testStandardOperations(self) -> None:
        self._rpn.alphabet = self._customizer.alphabet = Alphabet()
        self._customizer.add_space()
        self._customizer.add_standard_operations()

        self.assertEqual(self._rpn.get_rpn_expression('1 + 2 - 3 * 4 / 5'), '1 2 + 3 4 * 5 / -')
        self.assertAlmostEqual(self._rpn.solve(), 0.6)
        self.assertEqual(self._rpn.get_rpn_expression('-4 - 32 * 2 + 9 / 3 - 1'), '4 - 32 2 * - 9 3 / + 1 -')
        self.assertAlmostEqual(self._rpn.solve(), -66)
        self.assertEqual(self._rpn.get_rpn_expression('-3 * 8 + 99 / 1'), '3 - 8 * 99 1 / +')
        self.assertAlmostEqual(self._rpn.solve(), 75)

    def testBrackets(self) -> None:
        self._rpn.alphabet = self._customizer.alphabet = Alphabet()
        self._customizer.add_space()
        self._customizer.add_standard_operations()
        self._customizer.add_brackets()
        
        self.assertEqual(self._rpn.get_rpn_expression('(1 + 2) - 3 * (4 / 4)'), '1 2 + 3 4 4 / * -')
        self.assertAlmostEqual(self._rpn.solve(), 0)
        self.assertEqual(self._rpn.get_rpn_expression('-4 - 32 * (-2) + (9) / (4 - 1)'), '4 - 32 2 - * - 9 4 1 - / +')
        self.assertAlmostEqual(self._rpn.solve(), 63)
        self.assertEqual(self._rpn.get_rpn_expression('-3 * (8 + 99) / 1'), '3 - 8 99 + * 1 /')
        self.assertAlmostEqual(self._rpn.solve(), -321)
        self.assertEqual(self._rpn.get_rpn_expression('(1 / 2) * () (1 / 4)'), '1 2 / 1 4 / *')
        self.assertAlmostEqual(self._rpn.solve(), 0.125)

    def testSelfWrittenOperations(self) -> None:
        self._rpn.alphabet = self._customizer.alphabet = Alphabet()
        self._customizer.add_all()
        self._customizer.add_unary_operation('!', factorial, Fixation.POSTFIX)
        self._customizer.add_unary_operation('↑', self.inc, Fixation.POSTFIX)
        self._customizer.add_unary_operation('↓', self.dec, Fixation.PREFIX)
        self._customizer.add_binary_operation('^', pow, Priority.HIGH)

        self.assertEqual(self._rpn.get_rpn_expression('↓↓1↑↑↑↑ + 7 ^ 2 + 4!'), '1 ↓ ↑ ↑ ↑ ↑ ↓ 7 2 ^ + 4 ! +')
        self.assertAlmostEqual(self._rpn.solve(), 76)
        self.assertEqual(self._rpn.get_rpn_expression('-1↑! + ↓7 ^ (2 * (1 + 1)!)'), '1 - ↑ ! 7 ↓ 2 1 1 + ! * ^ +')
        self.assertAlmostEqual(self._rpn.solve(), 1297)
        self.assertEqual(self._rpn.get_rpn_expression('-4 ^ (1 / 2)'), '4 - 1 2 / ^')
        self.assertEqual(self._rpn.solve().imag, 2)  # Проверяем лишь мнимую часть числа, этого хватит.

    # Переопределение уже существующей операции не является ошибкой, поэтому с этим стоит быть осторожно.
    def testOperationOverride(self) -> None:
        self._rpn.alphabet = self._customizer.alphabet = Alphabet()
        self._customizer.add_all()

        # Переопределяем + как -, а - как +.
        self._customizer.add_binary_operation('+', sub, Priority.LOW)
        self._customizer.add_binary_operation('-', add, Priority.LOW)
        self.assertEqual(self._rpn.get_rpn_expression('100 + 50 + 25'), '100 50 + 25 +')
        self.assertAlmostEqual(self._rpn.solve(), 25)
        self.assertEqual(self._rpn.get_rpn_expression('100 - 50 - 25'), '100 50 - 25 -')
        self.assertAlmostEqual(self._rpn.solve(), 175)
        self.assertEqual(self._rpn.get_rpn_expression('100 * 2 + 50 * 2 - 25 * 2'), '100 2 * 50 2 * + 25 2 * -')
        self.assertAlmostEqual(self._rpn.solve(), 150)

        # Переопределяем скобки как инкременты.
        self._customizer.add_unary_operation('(', self.inc, Fixation.PREFIX)
        self._customizer.add_unary_operation(')', self.inc, Fixation.POSTFIX)
        self.assertEqual(self._rpn.get_rpn_expression('(4 * 3)'), '4 ( 3 ) *')
        self.assertAlmostEqual(self._rpn.solve(), 20)

        # Переопределяем пробел как +.
        self._customizer.add_binary_operation(' ', add, Priority.LOW)
        self.assertEqual(self._rpn.get_rpn_expression('4 89 29 1 8 3'), '4 89 + 29 + 1 + 8 + 3 +'.replace('+', ' '))
        self.assertAlmostEqual(self._rpn.solve(), 134)

    def testEmptyExpression(self) -> None:
        self._rpn.alphabet = self._customizer.alphabet = Alphabet()
        self._customizer.add_all()

        self.assertEqual(self._rpn.get_rpn_expression(''), '')
        self.assertEqual(self._rpn.solve(), None)
        self.assertEqual(self._rpn.get_rpn_expression('()'), '')
        self.assertEqual(self._rpn.solve(), None)
        self.assertEqual(self._rpn.get_rpn_expression('(())'), '')
        self.assertEqual(self._rpn.solve(), None)
        self.assertEqual(self._rpn.get_rpn_expression(' ( ) '), '')
        self.assertEqual(self._rpn.solve(), None)

    def testSyntaxError(self) -> None:
        # Найдены неизвестные символы:
        self._rpn.alphabet = Alphabet()
        self.assertRaises(SyntaxError, self._rpn.push_expression, '1 2')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '1+2')
        self.assertRaises(SyntaxError, self._rpn.push_expression, '1_2')

        # Нарушение языка выражений:
        self._customizer.alphabet = self._rpn.alphabet
        self._customizer.add_all()
        self._customizer.add_unary_operation('↑', self.inc, Fixation.POSTFIX)
        self._customizer.add_unary_operation('↓', self.dec, Fixation.PREFIX)
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
        self._rpn.alphabet = self._customizer.alphabet = Alphabet()
        self._customizer.add_all()

        # Добавление операции с недопустимым обозначением:
        self.assertRaises(ValueError, self._customizer.add_binary_operation, '', add, Priority.LOW)
        self.assertRaises(ValueError, self._customizer.add_binary_operation, '0', add, Priority.LOW)
        self.assertRaises(ValueError, self._customizer.add_binary_operation, 'add', add, Priority.LOW)

        # Нарушение соглашения об унарности/бинарности новой операции:
        self.assertRaises(ValueError, self._customizer.add_unary_operation, 'o', self.constant, Fixation.PREFIX)
        self.assertRaises(ValueError, self._customizer.add_unary_operation, '?',
                          self.ternary_operation, Fixation.PREFIX)
        self.assertRaises(ValueError, self._customizer.add_unary_operation, '+',
                          self.multiple_operation, Fixation.PREFIX)
        self.assertRaises(ValueError, self._customizer.add_binary_operation, 'o', self.constant, Priority.LOW)
        self.assertRaises(ValueError, self._customizer.add_binary_operation, '+', self.ternary_operation, Priority.LOW)
        self.assertRaises(ValueError, self._customizer.add_binary_operation, '+', self.multiple_operation, Priority.LOW)


if __name__ == '__main__':
    unittest.main()
