import re

import requests
from bs4 import BeautifulSoup

from utils import conf
from utils import convert_datetime_string

index_dict = {
    "WTI": "WTI",
    "휘발유": "GSOIL",
    "국제 금": "WGOLD",
    "국내 금": "LGOLD"
}


class ParserMarket:
    def __init__(self):
        self.url = conf('market')['url']
        self.currency = conf('market')['currency']
        self.table = 'market'
        self.items = []

    def parse(self):
        response = requests.get(self.url).text
        bs = BeautifulSoup(response, "html.parser")

        # Get exchange items
        table = bs.find('ul', id='exchangeList')
        for each in table.find_all('li'):
            if each.find('div', class_='head_info').attrs['class'][1] == 'point_up':
                status = each.find('span', class_='change').text.replace(" ", "")
            else:
                status = "-" + each.find('span', class_='change').text.replace(" ", "")

            item = dict(
                name=re.sub('[^a-zA-Z]+', '', each.find('span').text),
                price=each.find('span', class_='value').text,
                status=status,
                date=convert_datetime_string(each.find('span', class_='time').text)
            )
            self.items.append(item)

        # Get oil, gold items
        table = bs.find('ul', id='oilGoldList')
        for each in table.find_all('li'):
            if each.find('div', class_='head_info').attrs['class'][1] == 'point_up':
                status = each.find('span', class_='change').text.replace(" ", "")
            else:
                status = "-" + each.find('span', class_='change').text.replace(" ", "")

            item = dict(
                name=index_dict[each.find('span').text],
                price=each.find('span', class_='value').text,
                status=status,
                date=convert_datetime_string(each.find('span', class_='time').text)
            )
            self.items.append(item)

        return self.items
