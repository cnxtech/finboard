import requests

from utils import conf
from utils import convert_timestamp_mills


class ParserBithumb:
    def __init__(self):
        self.url = conf('bithumb')['url']
        self.currency = conf('bithumb')['currency']
        self.table = 'crypto'

    def parse(self, exchange, curr):
        response = requests.get(self.url + curr)
        result = response.json()["data"]

        item = dict(
            exchange=exchange,
            currency=curr.lower(),
            price=int(result["closing_price"]),
            volume=round(float(result["units_traded"])),
            date=convert_timestamp_mills(result['date'])
        )
        return item
