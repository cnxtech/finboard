import unittest

from crypto.bithumb import ParserBithumb
from crypto.coinone import ParserCoinone
from crypto.korbit import ParserKorbit


class TestCryptoCollector(unittest.TestCase):

    def test_bithumb(self):
        parser = ParserBithumb()
        for currency in parser.currency:
            parser.parse(currency)
            self.assertNotEqual(len(parser.items), 0)

    def test_coinone(self):
        parser = ParserCoinone()
        for currency in parser.currency:
            parser.parse(currency)
            self.assertNotEqual(len(parser.items), 0)

    def test_korbit(self):
        parser = ParserKorbit()
        for currency in parser.currency:
            parser.parse(currency)
            self.assertNotEqual(len(parser.items), 0)


if __name__ == '__main__':
    unittest.main()
