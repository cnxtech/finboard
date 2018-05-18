from multiprocessing import Manager
from multiprocessing import Process
from multiprocessing import Pool
from typing import List

import pandas as pd


class ParserStockPrice:
    def __init__(self, conf: dict):
        self.url = conf['url']
        self.currency = conf['currency']
        self.table = 'stock'
        self.items = Manager().list()

    def parse(self, curr: str):
        df = pd.read_html(self.url.format(curr), header=0)[0][:1]
        df = df.rename(columns={
            '날짜': 'date',
            '종가': 'close',
            '전일비': 'diff',
            '시가': 'open',
            '고가': 'high',
            '저가': 'low',
            '거래량': 'volume'
        })

        df[['close', 'diff', 'open', 'high', 'low', 'volume']] \
            = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)

        df['date'] = df['date'].apply(lambda d: str(pd.to_datetime(d)))
        item = df.to_dict(orient='records')[-1]
        item.update(name=curr)
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

    def get_all_items(self) -> List[dict]:
        pool = Pool()
        pool.map(self.parse, self.currency)
        return self.items
