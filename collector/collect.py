from __future__ import print_function

import boto3

from crypto.bithumb import ParserBithumb
from crypto.coinone import ParserCoinone
from crypto.korbit import ParserKorbit
from index.local import ParserLocal
from index.market import ParserMarket
from index.world import ParserWorld
from utils import conf, send_message


def handler(event, context):
    parser = {
        "bithumb": ParserBithumb,
        "coinone": ParserCoinone,
        "korbit": ParserKorbit,
        "local": ParserLocal,
        "market": ParserMarket,
        "world": ParserWorld,
    }

    target = event['target']
    parser = parser[target](conf(target))
    items = parser.get_items()
    print(*items, sep='\n')

    # Save to dynamodb
    dynamodb = boto3.resource('dynamodb', 'ap-northeast-2')
    table = dynamodb.Table(parser.table)

    with table.batch_writer() as batch:
        for each in items:
            batch.put_item(Item=each)
    send_message("monitoring", "{} collect finished!".format(target))


# For test
if __name__ == '__main__':
    handler({"target": "bithumb"}, None)
