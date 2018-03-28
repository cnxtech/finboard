import unittest

from stock.price import ParserStockPrice


class TestIndexCollector(unittest.TestCase):

    def test_price(self):
        parser = ParserStockPrice()
        for currency in parser.currency:
            parser.parse(currency)
            self.assertNotEqual(len(parser.items), 0)


if __name__ == '__main__':
    unittest.main()
