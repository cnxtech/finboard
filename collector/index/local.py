import requests
from bs4 import BeautifulSoup

from utils import conf
from utils import convert_datetime_format

index_dict = {
    "코스피": "KOSPI",
    "코스닥": "KOSDAQ",
    "코스피200": "KOSPI200"
}


class ParserLocal:
    def __init__(self):
        self.url = conf('local')['url']
        self.currency = conf('local')['currency']
        self.table = 'index'
        self.items = []

    def parse(self):
        response = requests.get(self.url).text
        bs = BeautifulSoup(response, "html.parser")
        date_str = ' '.join(bs.find('span', id='time1').text.split())

        for each in bs.find('div', class_='lft').find_all('li', onmouseover=True):
            rows = [i.text for i in each.find_all('span')]
            item = dict(
                name=index_dict[rows[0]],
                price=rows[1],
                status=rows[2].split()[0],
                rate=rows[2].split()[1][:-2],
                date=convert_datetime_format(date_str, "%Y.%m.%d %H:%M장중")
            )
            self.items.append(item)

        return self.items
