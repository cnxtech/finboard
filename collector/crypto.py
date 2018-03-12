import boto3

from crypto.bithumb import ParserBithumb
from crypto.coinone import ParserCoinone
from crypto.korbit import ParserKorbit


def collect(event, context):
    items = []
    parser_class = {
        "bithumb": ParserBithumb,
        "coinone": ParserCoinone,
        "korbit": ParserKorbit
    }

    for exchange, Parser in parser_class.items():
        parser = Parser()

        for curr in parser.currency:
            item = parser.parse(exchange, curr)
            items.append(item)

    # Save to dynamodb
    dynamodb = boto3.resource('dynamodb', 'ap-northeast-2')
    table = dynamodb.Table('crypto')

    with table.batch_writer() as batch:
        for each in items:
            batch.put_item(Item=each)
