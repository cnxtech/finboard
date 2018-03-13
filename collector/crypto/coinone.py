import requests

from utils import conf
from utils import convert_timestamp


class ParserCoinone:
    def __init__(self):
        self.url = conf('coinone')['url']
        self.currency = conf('coinone')['currency']

    def parse(self, exchange, curr):
        params = {"currency": curr}
        response = requests.get(self.url, params)
        result = response.json()

        item = dict(
            exchange=exchange,
            currency=curr,
            price=int(result["last"]),
            volume=round(float(result["volume"])),
            date=convert_timestamp(result['timestamp'])
        )
        return item
