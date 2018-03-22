from multiprocessing import Manager
from multiprocessing import Pool

import requests

from utils import conf
from utils import convert_timestamp_mills


class ParserBithumb:
    def __init__(self):
        self.url = conf('bithumb')['url']
        self.currency = conf('bithumb')['currency']
        self.table = 'crypto'
        self.items = Manager().list()

    def parse(self, curr):
        response = requests.get(self.url + curr)
        result = response.json()["data"]

        item = dict(
            exchange="bithumb",
            currency=curr.lower(),
            price=int(result["closing_price"]),
            volume=round(float(result["units_traded"])),
            date=convert_timestamp_mills(result['date'])
        )
        self.items.append(item)

    def get_items(self):
        pool = Pool()
        pool.map(self.parse, self.currency)
        return self.items
