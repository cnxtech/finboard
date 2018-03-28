import unittest

from collector.utils import conf
from crypto.bithumb import ParserBithumb
from crypto.coinone import ParserCoinone
from crypto.korbit import ParserKorbit


class TestCryptoCollector(unittest.TestCase):

    def setUp(self):
        self.bithumb_conf = conf('bithumb')
        self.coinone_conf = conf('coinone')
        self.korbit_conf = conf('korbit')

    def test_bithumb(self):
        parser = ParserBithumb(self.bithumb_conf)
        for currency in parser.currency:
            parser.parse(currency)
            self.assertNotEqual(len(parser.items), 0)

    def test_coinone(self):
        parser = ParserCoinone(self.coinone_conf)
        for currency in parser.currency:
            parser.parse(currency)
            self.assertNotEqual(len(parser.items), 0)

    def test_korbit(self):
        parser = ParserKorbit(self.korbit_conf)
        for currency in parser.currency:
            parser.parse(currency)
            self.assertNotEqual(len(parser.items), 0)


if __name__ == '__main__':
    unittest.main()
