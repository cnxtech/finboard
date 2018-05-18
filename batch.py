import os

import boto3
import pandas as pd

from collector.stock.code import ParserStockCode
from collector.stock.price import ParserStockPrice
from collector.utils import conf
from lib import env


def collect_stock_code(path: str):
    parser = ParserStockCode(conf('code'))
    df = parser.get_items()
    df.to_parquet(path, engine='pyarrow')

    # Save to S3
    s3 = boto3.client('s3', env.REGION)
    s3.upload_file(path, env.BUCKET, 'code.parquet')
    print("collect finished!")


def collect_stock_price(path: str):
    # Get stock codes
    df = pd.read_parquet(path, engine='pyarrow')
    codes = df.code.values

    parser = ParserStockPrice(conf('stock'))
    parser.currency = codes
    items = parser.get_all_items()
    print("collect {} items".format(len(items)))

    # Save to dynamodb
    dynamodb = boto3.resource('dynamodb', 'ap-northeast-2')
    table = dynamodb.Table(parser.table)

    with table.batch_writer() as batch:
        for each in items:
            batch.put_item(Item=each)
    print("collect finished!")


def run_batch():
    dist_dir = os.path.join(os.getcwd(), 'dist/')
    dist_path = "{}code.parquet".format(dist_dir)

    # Run batch collector
    # collect_stock_code(dist_path)
    collect_stock_price(dist_path)
