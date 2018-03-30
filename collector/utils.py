import json
import os
import re
from datetime import datetime

import pandas as pd

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))


def conf(target: str) -> dict:
    path = os.path.join(PROJECT_DIR, 'config.json')
    with open(path, 'r') as f:
        config = json.load(f)
    return config[target]


def add_status(cls_name: str, status: str, value: str) -> str:
    status = status.replace(" ", "")
    if cls_name == value:
        return "-" + status
    else:
        return status


def calculate_ratio(status: str, price: str) -> str:
    return str(round((float(status) / float(price)) * 100, 2))


def current_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def convert_datetime_string(date_str: str) -> str:
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    date_str = ' '.join(hangul.findall(date_str))
    return str(pd.to_datetime(date_str))


def convert_timestamp(timestamp: str) -> str:
    time = datetime.fromtimestamp(int(timestamp))
    return time.strftime("%Y-%m-%d %H:%M:%S")


def convert_timestamp_mills(timestamp: str) -> str:
    time = datetime.fromtimestamp(int(timestamp) / 1000.0)
    return time.strftime("%Y-%m-%d %H:%M:%S")
