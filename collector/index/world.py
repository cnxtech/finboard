import requests
from bs4 import BeautifulSoup

from utils import calculate_ratio
from utils import conf
from utils import convert_datetime_string

index_dict = {
    "DJI@DJI": "DJI",
    "NII@NI225": "NII",
    "LNS@FTSE100": "FTSE",
    "NAS@IXIC": "NAS",
    "SHS@000001": "SHS",
    "PAS@CAC40": "CAC",
    "SPI@SPX": "SPI",
    "HSI@HSI": "HSI",
    "XTR@DAX30": "DAX",
    "INI@BSE30": "SENSEX"
}


class ParserWorld:
    def __init__(self):
        self.url = conf('world')['url']
        self.currency = conf('world')['currency']
        self.table = 'index'
        self.items = []

    def parse(self):
        for curr in self.currency:
            params = {"symbol": curr}
            response = requests.get(self.url, params).text
            bs = BeautifulSoup(response, "html.parser")

            rows = bs.find('table', id='dayTable').find('tbody')
            price = rows.find('span').text

            if rows.find('tr').attrs['class'][0] == 'point_up':
                status = rows.find('span', class_='point_status').text
            else:
                status = "-" + rows.find('span', class_='point_status').text

            item = dict(
                name=index_dict[curr],
                date=convert_datetime_string(rows.find('td').text),
                price=price,
                status=status,
                rate=calculate_ratio(status, price.replace(",", ""))
            )
            self.items.append(item)

        return self.items
