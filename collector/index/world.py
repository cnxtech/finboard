from multiprocessing import Manager
from multiprocessing import Process
from typing import List

import requests
from bs4 import BeautifulSoup

from utils import add_status
from utils import calculate_ratio
from utils import convert_datetime_string


class ParserWorld:
    def __init__(self, conf: dict):
        self.url = conf['url']
        self.currency = conf['currency']
        self.table = 'index'
        self.items = Manager().list()

    def parse(self, curr):
        symbol, name = curr.split()
        params = {"symbol": symbol}
        response = requests.get(self.url, params).text
        bs = BeautifulSoup(response, "html.parser")

        rows = bs.find('table', id='dayTable').find('tbody')
        price = rows.find('span').text
        status = add_status(rows.find('tr').attrs['class'][0],
                            rows.find('span', class_='point_status').text, "point_dn")

        item = dict(
            name=name,
            date=convert_datetime_string(rows.find('td').text),
            price=float(price.replace(",", "")),
            status=status,
            rate=calculate_ratio(status, price.replace(",", ""))
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
