import json
import os
from datetime import datetime


def conf(target):
    path = os.path.join(os.getcwd(), 'config.json')
    with open(path, 'r') as f:
        config = json.load(f)
    return config[target]


def current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def convert_datetime_format(date_str, form):
    date_obj = datetime.strptime(date_str, form)
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")


def convert_timestamp(timestamp):
    time = datetime.fromtimestamp(int(timestamp))
    return time.strftime("%Y-%m-%d %H:%M:%S")


def convert_timestamp_mills(timestamp):
    time = datetime.fromtimestamp(int(timestamp) / 1000.0)
    return time.strftime("%Y-%m-%d %H:%M:%S")
