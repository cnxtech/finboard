from multiprocessing import Manager
from multiprocessing import Process
from typing import List

import requests

from utils import convert_timestamp_mills


class ParserBithumb:
    def __init__(self, conf: dict):
        self.url = conf['url']
        self.currency = conf['currency']
        self.table = 'crypto'
        self.items = Manager().list()

    def parse(self, curr: str):
        response = requests.get(self.url + curr)
        result = response.json()["data"]

        item = dict(
            exchange="bithumb",
            name=curr.lower(),
            price=int(result["closing_price"]),
            volume=round(float(result["units_traded"])),
            date=convert_timestamp_mills(result['date'])
        )
        self.items.append(item)

    def get_items(self) -> List[dict]:
        procs = []
        for _index, curr in enumerate(self.currency):
            proc = Process(target=self.parse, args=(curr,))
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()

        return self.items
