from index.exchange import ParserExchange
from index.local import ParserLocal
from index.world import ParserWorld


def test_exchange():
    parser = ParserExchange()
    result = parser.parse()
    assert len(result) != 0


def test_local():
    parser = ParserLocal()
    result = parser.parse()
    assert len(result) != 0


def test_world():
    parser = ParserWorld()
    result = parser.parse()
    assert len(result) != 0
