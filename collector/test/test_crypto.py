import unittest

from crypto.bithumb import ParserBithumb
from crypto.coinone import ParserCoinone
from crypto.korbit import ParserKorbit


class TestStringMethods(unittest.TestCase):

    def test_bithumb(self):
        parser = ParserBithumb()
        for currency in parser.currency:
            result = parser.parse('bithumb', currency)
            self.assertTrue(isinstance(result, dict))

    def test_coinone(self):
        parser = ParserCoinone()
        for currency in parser.currency:
            result = parser.parse('coinone', currency)
            self.assertTrue(isinstance(result, dict))

    def test_korbit(self):
        parser = ParserKorbit()
        for currency in parser.currency:
            result = parser.parse('korbit', currency)
            self.assertTrue(isinstance(result, dict))


if __name__ == '__main__':
    unittest.main()
