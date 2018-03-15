from index.exchange import ParserExchange


def test_exchange():
    parser = ParserExchange()
    result = parser.parse()
    assert isinstance(result, list)
