import requests

from utils import conf
from utils import convert_timestamp_mills


class ParserKorbit:
    def __init__(self):
        self.url = conf('korbit')['url']
        self.currency = conf('korbit')['currency']
        self.table = 'crypto'

    def parse(self, exchange, curr):
        params = {"currency_pair": curr}
        response = requests.get(self.url, params)
        result = response.json()

        item = dict(
            exchange=exchange,
            currency=curr.replace("_krw", ""),
            price=int(result["last"]),
            volume=round(float(result["volume"])),
            date=convert_timestamp_mills(result['timestamp'])
        )
        return item
