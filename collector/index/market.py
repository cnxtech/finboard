import re

import requests
from bs4 import BeautifulSoup

from typing import List
from utils import add_status
from utils import convert_datetime_string

INDEX_DICT = {
    "WTI": "WTI",
    "휘발유": "GSOIL",
    "국제 금": "WGOLD",
    "국내 금": "LGOLD"
}


class ParserMarket:
    def __init__(self, conf: dict):
        self.url = conf['url']
        self.currency = conf['currency']
        self.table = 'market'
        self.items = []

    def parse(self):
        response = requests.get(self.url).text
        bs = BeautifulSoup(response, "html.parser")

        # Get exchange items
        table = bs.find('ul', id='exchangeList')
        for each in table.find_all('li'):
            status = add_status(each.find('div', class_='head_info').attrs['class'][1],
                                each.find('span', class_='change').text, "point_dn")

            item = dict(
                name=re.sub('[^a-zA-Z]+', '', each.find('span').text),
                price=each.find('span', class_='value').text.replace(",", ""),
                status=status,
                date=convert_datetime_string(each.find('span', class_='time').text)
            )
            self.items.append(item)

        # Get oil, gold items
        table = bs.find('ul', id='oilGoldList')
        for each in table.find_all('li'):
            status = add_status(each.find('div', class_='head_info').attrs['class'][1],
                                each.find('span', class_='change').text, "point_dn")

            item = dict(
                name=INDEX_DICT[each.find('span').text],
                price=each.find('span', class_='value').text.replace(",", ""),
                status=status,
                date=convert_datetime_string(each.find('span', class_='time').text)
            )
            self.items.append(item)

    def get_items(self) -> List[dict]:
        self.parse()
        return self.items
