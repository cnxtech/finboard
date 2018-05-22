from typing import List

import requests
from bs4 import BeautifulSoup

from utils import add_status
from utils import current_datetime

INDEX_DICT = {
    "코스피": "KOSPI",
    "코스닥": "KOSDAQ",
    "코스피200": "KOSPI200"
}


class ParserLocal:
    def __init__(self, conf: dict):
        self.url = conf['url']
        self.currency = conf['currency']
        self.table = 'index'
        self.items = []

    def parse(self):
        response = requests.get(self.url).text
        bs = BeautifulSoup(response, "html.parser")

        for each in bs.find('div', class_='lft').find_all('li', onmouseover=True):
            rows = [i.text for i in each.find_all('span')]
            tmp = rows[2].split()
            status = add_status(tmp[1][0], tmp[0], "-")

            item = dict(
                name=INDEX_DICT[rows[0]],
                price=rows[1].replace(",", ""),
                status=status,
                rate=tmp[1][:-3].replace("+", ""),
                date=current_datetime()
            )
            self.items.append(item)

    def get_items(self) -> List[dict]:
        self.parse()
        return self.items
