import re

import requests
from bs4 import BeautifulSoup

from utils import conf
from utils import current_datetime


class ParserExchange:
    def __init__(self):
        self.url = conf('exchange')['url']
        self.currency = conf('exchange')['currency']
        self.table = 'exchange'
        self.items = []

    def parse(self):
        response = requests.get(self.url).text
        bs = BeautifulSoup(response, "html.parser")

        table = bs.find('table', class_='tbl_exchange')
        rows = table.find('tbody').find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            cols = [element.text.strip() for element in cols]
            cols[0] = re.sub('[^a-zA-Z]+', '', cols[0])

            if cols[0] in self.currency:
                item = dict(
                    currency=cols[0],
                    rate=cols[1],
                    date=current_datetime()
                )
                self.items.append(item)

        return self.items
