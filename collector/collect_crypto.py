import boto3

from crypto.bithumb import ParserBithumb
from crypto.coinone import ParserCoinone
from crypto.korbit import ParserKorbit


def collect(event, context):
    parser = {
        "bithumb": ParserBithumb,
        "coinone": ParserCoinone,
        "korbit": ParserKorbit
    }

    exchange = event['type']
    parser = parser[exchange]()
    items = []

    for curr in parser.currency:
        item = parser.parse(exchange, curr)
        items.append(item)
        print(item)

    # Save to dynamodb
    dynamodb = boto3.resource('dynamodb', 'ap-northeast-2')
    table = dynamodb.Table('test')

    with table.batch_writer() as batch:
        for each in items:
            batch.put_item(Item=each)

    print("collect crypto finished!")
