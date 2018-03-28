from multiprocessing import Manager
from multiprocessing import Pool

import pandas as pd

from utils import conf

index_dict = {
    "035420": "NAVER",
    "035720": "KAKAO",
    "000660": "HYNIX",
    "005930": "SS_ELECTRON",
    "068270": "CELLTRION"
}

columns = {
    '날짜': 'date',
    '종가': 'close',
    '전일비': 'diff',
    '시가': 'open',
    '고가': 'high',
    '저가': 'low',
    '거래량': 'volume'
}


class ParserStockPrice:
    def __init__(self):
        self.url = conf('stock')['url']
        self.currency = conf('stock')['currency']
        self.table = 'stock'
        self.items = Manager().list()

    def parse(self, curr):
        df = pd.read_html(self.url.format(curr), header=0)[0][:1]
        df = df.rename(columns=columns)

        df[['close', 'diff', 'open', 'high', 'low', 'volume']] \
            = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)

        df['date'] = df['date'].apply(lambda d: str(pd.to_datetime(d)))
        item = df.to_dict(orient='records')[-1]
        item.update(name=index_dict[curr])
        self.items.append(item)

    def get_items(self):
        pool = Pool()
        pool.map(self.parse, self.currency)
        return self.items
