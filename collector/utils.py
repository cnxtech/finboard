import json
import os
import re
from datetime import datetime

import pandas as pd


def conf(target):
    path = os.path.join(os.getcwd(), 'config.json')
    with open(path, 'r') as f:
        config = json.load(f)
    return config[target]


def add_status(cls_name, status, value):
    status = status.replace(" ", "")
    if cls_name == value:
        return "-" + status
    else:
        return status


def calculate_ratio(status, price):
    return str(round((float(status) / float(price)) * 100, 2))


def current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def convert_datetime_string(date_str: str):
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    date_str = ' '.join(hangul.findall(date_str))
    return str(pd.to_datetime(date_str))


def convert_timestamp(timestamp):
    time = datetime.fromtimestamp(int(timestamp))
    return time.strftime("%Y-%m-%d %H:%M:%S")


def convert_timestamp_mills(timestamp):
    time = datetime.fromtimestamp(int(timestamp) / 1000.0)
    return time.strftime("%Y-%m-%d %H:%M:%S")
