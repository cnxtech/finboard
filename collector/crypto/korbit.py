from multiprocessing import Manager
from multiprocessing import Pool

import requests

from utils import convert_timestamp_mills


class ParserKorbit:
    def __init__(self, conf):
        self.url = conf['url']
        self.currency = conf['currency']
        self.table = 'crypto'
        self.items = Manager().list()

    def parse(self, curr):
        params = {"currency_pair": curr}
        response = requests.get(self.url, params)
        result = response.json()

        item = dict(
            exchange="korbit",
            currency=curr.replace("_krw", ""),
            price=int(result["last"]),
            volume=round(float(result["volume"])),
            date=convert_timestamp_mills(result['timestamp'])
        )
        self.items.append(item)

    def get_items(self):
        pool = Pool()
        pool.map(self.parse, self.currency)
        return self.items
