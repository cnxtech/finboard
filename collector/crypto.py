import requests
import boto3

from .utils import convert_timestamp

url = 'https://api.bithumb.com/public/ticker/{}'
currency = ["BTC", "ETH"]


def collect_crypto():
    items = []
    for curr in currency:
        response = requests.get(url.format(curr))
        result = response.json()["data"]

        item = dict(
            currency=curr,
            price=int(result["closing_price"]),
            volume=round(float(result["units_traded"])),
            date=convert_timestamp(result['date'])
        )
        items.append(item)

    # Save to dynamodb
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    table = dynamodb.Table('crypto')

    with table.batch_writer() as batch:
        for each in items:
            batch.put_item(Item=each)
