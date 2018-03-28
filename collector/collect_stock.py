import boto3

from stock.price import ParserStockPrice


def collect(event, context):
    parser = {
        "price": ParserStockPrice
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
    collect({"target": "price"}, None)
