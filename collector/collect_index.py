import boto3

from index.exchange import ParserExchange


def collect(event, context):
    parser = {
        "exchange": ParserExchange,
    }

    target = event['target']
    parser = parser[target]()
    items = parser.parse()
    print(*items, sep='\n')

    # Save to dynamodb
    dynamodb = boto3.resource('dynamodb', 'ap-northeast-2')
    table = dynamodb.Table(target)

    with table.batch_writer() as batch:
        for each in items:
            batch.put_item(Item=each)
    print("collect index finished!")


# For test
if __name__ == '__main__':
    collect({"type": "exchange"}, None)
