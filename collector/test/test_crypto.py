from crypto.bithumb import ParserBithumb
from crypto.coinone import ParserCoinone
from crypto.korbit import ParserKorbit


def test_bithumb():
    parser = ParserBithumb()
    for currency in parser.currency:
        result = parser.parse('bithumb', currency)
        assert isinstance(result, dict)


def test_coinone():
    parser = ParserCoinone()
    for currency in parser.currency:
        result = parser.parse('coinone', currency)
        assert isinstance(result, dict)


def test_korbit():
    parser = ParserKorbit()
    for currency in parser.currency:
        result = parser.parse('korbit', currency)
        assert isinstance(result, dict)
