import argparse
import json
import os
import zipfile
from pprint import pprint
from typing import Set

import boto3
import pip

from lib import env


class Manager(object):
    """Rogers-Collector management utility"""

    def __init__(self):
        self.lambda_dir = os.getcwd()
        self.collector_dir = os.path.join(os.getcwd(), 'collector')
        self.streamer_dir = os.path.join(os.getcwd(), 'streamer')

    @property
    def commands(self) -> Set[str]:
        """Return set of available management commands"""
        return {'create', 'update', 'invoke'}

    def run(self, command: str, payload: str) -> None:
        """Execute one of the available commands"""
        getattr(self, command)(payload)

    @staticmethod
    def make_zipfile(directory, zf) -> None:
        for root, _dirs, files in os.walk(directory):
            for filename in files:
                if not filename.endswith('.pyc'):
                    os.chmod(os.path.join(root, filename), 0o644)
                    zf.write(
                        os.path.join(root, filename),
                        os.path.join(
                            root.replace(directory, ''),
                            filename
                        )
                    )

    @staticmethod
    def upload_to_s3() -> None:
        s3 = boto3.client('s3', env.REGION)
        s3.upload_file('collector.zip', env.BUCKET, 'collector.zip')
        s3.upload_file('streamer.zip', env.BUCKET, 'streamer.zip')

    def append_packages(self, directory: str, target: str) -> None:
        dist_path = os.path.join(self.lambda_dir, 'dist/')
        if not os.path.exists(dist_path):
            os.makedirs(dist_path)
        pip_args = [
            'install',
            '-r',
            os.path.join(directory, 'requirements.txt'),
            '-t',
            os.path.join('dist')
        ]
        pip.main(pip_args)

        # Append dist packages to zipfile
        zipf = zipfile.ZipFile(target, 'a', zipfile.ZIP_DEFLATED)
        self.make_zipfile(dist_path, zipf)
        zipf.close()
        os.system('rm -rf {}'.format(dist_path))

    def refresh(self) -> None:
        # Make collector to zipfile
        zipf = zipfile.ZipFile('collector.zip', 'w', zipfile.ZIP_DEFLATED)
        self.make_zipfile(os.path.join(self.lambda_dir, 'collector/'), zipf)
        zipf.close()
        self.append_packages('collector', 'collector.zip')

        # Make streamer to zipfile
        zipf = zipfile.ZipFile('streamer.zip', 'w', zipfile.ZIP_DEFLATED)
        self.make_zipfile(os.path.join(self.lambda_dir, 'streamer/'), zipf)
        zipf.close()
        self.append_packages('streamer', 'streamer.zip')

        # Upload and update lambda function
        self.upload_to_s3()

    def create(self, _payload: str) -> None:
        self.refresh()

        lambda_f = boto3.client('lambda', 'ap-northeast-2')
        pprint(
            lambda_f.create_function(
                FunctionName='collector',
                Runtime='python3.6',
                Role=env.COLLECTOR_ROLE,
                Timeout=10,
                Handler='collect.handler',
                Code={
                    'S3Bucket': env.BUCKET,
                    'S3Key': 'collector.zip'
                }
            ))

        pprint(lambda_f.create_function(
            FunctionName='streamer',
            Runtime='python3.6',
            Role=env.STREAMER_ROLE,
            Timeout=10,
            Handler='stream.handler',
            Code={
                'S3Bucket': env.BUCKET,
                'S3Key': 'streamer.zip'
            }
        ))

    def update(self, _payload: str) -> None:
        self.refresh()

        lambda_f = boto3.client('lambda', 'ap-northeast-2')
        pprint(lambda_f.update_function_code(
            FunctionName='collector',
            S3Bucket=env.BUCKET,
            S3Key='collector.zip'
        ))

        pprint(lambda_f.update_function_code(
            FunctionName='streamer',
            S3Bucket=env.BUCKET,
            S3Key='streamer.zip'
        ))

    @staticmethod
    def invoke(payload: str) -> None:
        payload = {"target": payload}
        lambda_f = boto3.client('lambda', 'ap-northeast-2')
        pprint(lambda_f.invoke(
            FunctionName='collector',
            InvocationType='RequestResponse',
            Payload=bytes(json.dumps(payload, ensure_ascii=False).encode('utf8'))
        ))


if __name__ == "__main__":
    manager = Manager()

    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=sorted(manager.commands))
    parser.add_argument('--payload')
    args = parser.parse_args()

    manager.run(args.command, args.payload)
    print("job finished!")
