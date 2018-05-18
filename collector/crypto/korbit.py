from multiprocessing import Manager
from multiprocessing import Process
from typing import List

import requests

from utils import convert_timestamp_mills


class ParserKorbit:
    def __init__(self, conf: dict):
        self.url = conf['url']
        self.currency = conf['currency']
        self.table = 'crypto'
        self.items = Manager().list()

    def parse(self, curr: str):
        params = {"currency_pair": curr}
        response = requests.get(self.url, params)
        result = response.json()

        item = dict(
            exchange="korbit",
            name=curr.replace("_krw", ""),
            price=int(result["last"]),
            volume=round(float(result["volume"])),
            date=convert_timestamp_mills(result['timestamp'])
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
