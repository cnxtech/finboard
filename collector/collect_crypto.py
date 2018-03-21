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

    target = event['target']
    parser = parser[target]()
    items = []

    for curr in parser.currency:
        item = parser.parse(target, curr)
        items.append(item)
    print(*items, sep='\n')

    # Save to dynamodb
    dynamodb = boto3.resource('dynamodb', 'ap-northeast-2')
    table = dynamodb.Table(parser.table)

    with table.batch_writer() as batch:
        for each in items:
            batch.put_item(Item=each)
    print("collect crypto finished!")


# For test
if __name__ == '__main__':
    collect({"target": "bithumb"}, None)
