import argparse
import json
import os
import zipfile
from typing import Set

import boto3
import pip


class Manager(object):
    """Rogers-Collector management utility"""

    def __init__(self):
        self.lambda_dir = os.getcwd()

    @property
    def commands(self) -> Set[str]:
        """Return set of available management commands"""
        return {'create', 'update', 'invoke'}

    def run(self, command: str, payload: str=None) -> None:
        """Execute one of the available commands"""
        if command == 'invoke':
            getattr(self, command)(payload)
        else:
            getattr(self, command)()

    @staticmethod
    def pip_install(directory: str) -> None:
        pip_args = [
            'install',
            '-r',
            os.path.join(directory, 'requirements.txt'),
            '-t',
            'dist'
        ]
        pip.main(pip_args)

    @staticmethod
    def make_zipfile(directory, zf):
        for root, dirs, files in os.walk(directory):
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
    def upload_to_s3():
        s3 = boto3.client('s3', 'ap-northeast-2')
        s3.upload_file('collector.zip', 'rogers-collector', 'collector.zip')

    def create(self):
        self.pip_install(self.lambda_dir)

        # Make collector to zipfile
        zipf = zipfile.ZipFile('collector.zip', 'w', zipfile.ZIP_DEFLATED)
        self.make_zipfile(os.path.join(self.lambda_dir, 'collector/'), zipf)
        zipf.close()

        # Append dist packages to zipfile
        zipf = zipfile.ZipFile('collector.zip', 'a', zipfile.ZIP_DEFLATED)
        self.make_zipfile(os.path.join(self.lambda_dir, 'dist/'), zipf)
        zipf.close()

        # Upload and update lambda function
        self.upload_to_s3()

        lambda_f = boto3.client('lambda', 'ap-northeast-2')
        res = lambda_f.create_function(
            FunctionName='collect',
            Runtime='python3.6',
            Role=os.getenv('LAMBDA_ROLE'),
            Timeout=3,
            Handler='collect.handler',
            Code={
                'S3Bucket': 'rogers-collector',
                'S3Key': 'collector.zip'
            }
        )
        print(res)

    def update(self):
        self.pip_install(self.lambda_dir)

        # Make collector to zipfile
        zipf = zipfile.ZipFile('collector.zip', 'w', zipfile.ZIP_DEFLATED)
        self.make_zipfile(os.path.join(self.lambda_dir, 'collector/'), zipf)
        zipf.close()

        # Append dist packages to zipfile
        zipf = zipfile.ZipFile('collector.zip', 'a', zipfile.ZIP_DEFLATED)
        self.make_zipfile(os.path.join(self.lambda_dir, 'dist/'), zipf)
        zipf.close()

        # Upload and update lambda function
        self.upload_to_s3()

        lambda_f = boto3.client('lambda', 'ap-northeast-2')
        res = lambda_f.update_function_code(
            FunctionName='collect',
            S3Bucket='rogers-collector',
            S3Key='collector.zip'
        )
        print(res)

    @staticmethod
    def invoke(payload):
        payload = {"target": payload}
        lambda_f = boto3.client('lambda', 'ap-northeast-2')
        res = lambda_f.invoke(
            FunctionName='collect',
            InvocationType='RequestResponse',
            Payload=bytes(json.dumps(payload, ensure_ascii=False).encode('utf8'))
        )
        print(res)


if __name__ == "__main__":
    manager = Manager()

    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=sorted(manager.commands))
    parser.add_argument('--payload')
    args = parser.parse_args()

    manager.run(args.command)
    print("action finished!")
