import unittest

from utils import conf
from stock.price import ParserStockPrice


class TestIndexCollector(unittest.TestCase):

    def setUp(self):
        self.price_conf = conf('stock')

    def test_price(self):
        parser = ParserStockPrice(self.price_conf)
        for currency in parser.currency:
            parser.parse(currency)
            self.assertNotEqual(len(parser.items), 0)


if __name__ == '__main__':
    unittest.main()
