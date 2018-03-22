import boto3

from index.local import ParserLocal
from index.market import ParserMarket
from index.world import ParserWorld


def collect(event, context):
    parser = {
        "local": ParserLocal,
        "market": ParserMarket,
        "world": ParserWorld
    }

    target = event['target']
    parser = parser[target]()
    items = parser.get_items()
    print(*items, sep='\n')

    # Save to dynamodb
    dynamodb = boto3.resource('dynamodb', 'ap-northeast-2')
    table = dynamodb.Table(parser.table)

    with table.batch_writer() as batch:
        for each in items:
            batch.put_item(Item=each)
    print("collect index finished!")


# For test
if __name__ == '__main__':
    collect({"target": "world"}, None)
