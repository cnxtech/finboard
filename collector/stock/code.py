from typing import List

import pandas as pd

INDEX_DICT = {
    'kospi': 'stockMkt',
    'kosdaq': 'kosdaqMkt',
    'konex': 'konexMkt'
}


class ParserStockCode:
    def __init__(self, conf: dict):
        self.url = conf['url']
        self.currency = conf['currency']
        self.table = 'code'
        self.overwrite = True
        self.items = []

    def parse(self):
        for each in self.currency:
            df = pd.read_html(self.url.format(INDEX_DICT[each]), header=0)[0]
            df = df.rename(columns={
                '회사명': 'name',
                '종목코드': 'code',
                '업종': 'industry',
                '주요제품': 'product',
                '상장일': 'opening_date',
                '결산월': 'closing_month',
                '대표자명': 'ceo',
                '홈페이지': 'homepage',
                '지역': 'local'
            })
            df['market'] = each
            df.code = df.code.map('{:06d}'.format)
            self.items.append(df.fillna('-'))

    def get_items(self) -> pd.DataFrame:
        self.parse()
        return pd.concat(self.items)
