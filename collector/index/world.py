import requests
from bs4 import BeautifulSoup

from utils import conf
from utils import convert_datetime_format

index_dict = {
    "다우 산업": "DJI",
    "니케이 225": "NII",
    "영국 FTSE 100": "FTSE",
    "나스닥 종합": "NAS",
    "상해종합": "SHS",
    "프랑스 CAC 40": "CAC",
    "S&P500": "SPI",
    "항셍": "HSI",
    "독일 DAX": "DAX"
}


class ParserWorld:
    def __init__(self):
        self.url = conf('world')['url']
        self.currency = conf('world')['currency']
        self.table = 'index'
        self.items = []

    def parse(self):
        response = requests.get(self.url).text
        bs = BeautifulSoup(response, "html.parser")

        for each in bs.find_all('div', class_='data'):
            for row in each.find_all('li'):
                date_str = row.find('span', class_='date').text
                item = dict(
                    name=index_dict[row.find('span').text],
                    price=row.find('strong').text,
                    status=row.find('em').text,
                    rate=row.find('dd', class_='point_status').find('span').text,
                    date=convert_datetime_format(date_str, "%Y.%m.%d %H:%M 기준")
                )
                self.items.append(item)

        return self.items
