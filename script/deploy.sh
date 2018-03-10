#!/usr/bin/env bash

pip install -r requirements.txt -t dist
zip -9 collector.zip collector
zip -r9 collector.zip dist
aws s3 cp collector.zip s3://rogers-collector/collector.zip

echo "upload to s3 finished!"