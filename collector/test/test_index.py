import unittest

from index.exchange import ParserExchange
from index.local import ParserLocal
from index.world import ParserWorld


class TestStringMethods(unittest.TestCase):

    def test_exchange(self):
        parser = ParserExchange()
        result = parser.parse()
        self.assertNotEqual(len(result), 0)

    def test_local(self):
        parser = ParserLocal()
        result = parser.parse()
        self.assertNotEqual(len(result), 0)

    def test_world(self):
        parser = ParserWorld()
        result = parser.parse()
        self.assertNotEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
