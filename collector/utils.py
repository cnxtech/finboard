from datetime import datetime


def convert_timestamp(timestamp):
    time = datetime.fromtimestamp(int(timestamp)/1000.0)
    return time.strftime("%Y-%m-%d %H:%M:%S")
