import unittest

from utils import conf
from index.local import ParserLocal
from index.market import ParserMarket
from index.world import ParserWorld


class TestIndexCollector(unittest.TestCase):

    def setUp(self):
        self.local_conf = conf('local')
        self.market_conf = conf('market')
        self.world_conf = conf('world')

    def test_local(self):
        parser = ParserLocal(self.local_conf)
        parser.parse()
        self.assertNotEqual(len(parser.items), 0)

    def test_market(self):
        parser = ParserMarket(self.market_conf)
        parser.parse()
        self.assertNotEqual(len(parser.items), 0)

    def test_world(self):
        parser = ParserWorld(self.world_conf)
        for currency in parser.currency:
            parser.parse(currency)
            self.assertNotEqual(len(parser.items), 0)


if __name__ == '__main__':
    unittest.main()
