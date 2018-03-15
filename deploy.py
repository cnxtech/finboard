import os
import pip
import json
import zipfile
import boto3
import argparse


def pip_install(directory):
    pip_args = [
        'install',
        '-r',
        os.path.join(directory, 'requirements.txt'),
        '-t',
        'dist'
    ]
    pip.main(pip_args)


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


def upload_to_s3():
    s3 = boto3.client('s3', 'ap-northeast-2')
    s3.upload_file('collector.zip', 'rogers-collector', 'collector.zip')


def create_lambda_function(function_name):
    lambda_f = boto3.client('lambda', 'ap-northeast-2')
    res = lambda_f.create_function(
        FunctionName='collect_{}'.format(function_name),
        Runtime='python3.6',
        Role=os.getenv('LAMBDA_ROLE'),
        Timeout=3,
        Handler='collect_{}.collect'.format(function_name),
        Code={
            'S3Bucket': 'rogers-collector',
            'S3Key': 'collector.zip'
        }
    )
    print(res)


def invoke_lambda_function(function_name, payload):
    payload = {"target": payload}
    lambda_f = boto3.client('lambda', 'ap-northeast-2')
    res = lambda_f.invoke(
        FunctionName='collect_{}'.format(function_name),
        InvocationType='RequestResponse',
        Payload=bytes(json.dumps(payload, ensure_ascii=False).encode('utf8'))
    )
    print(res)


def update_lambda_function(function_name):
    lambda_dir = os.getcwd()
    pip_install(lambda_dir)

    # Make collector to zipfile
    zipf = zipfile.ZipFile('collector.zip', 'w', zipfile.ZIP_DEFLATED)
    make_zipfile(os.path.join(lambda_dir, 'collector/'), zipf)
    zipf.close()

    # Append dist packages to zipfile
    zipf = zipfile.ZipFile('collector.zip', 'a', zipfile.ZIP_DEFLATED)
    make_zipfile(os.path.join(lambda_dir, 'dist/'), zipf)
    zipf.close()

    # Upload and update lambda function
    upload_to_s3()

    lambda_f = boto3.client('lambda', 'ap-northeast-2')
    res = lambda_f.update_function_code(
        FunctionName='collect_{}'.format(function_name),
        S3Bucket='rogers-collector',
        S3Key='collector.zip'
    )
    print(res)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", required=True)
    parser.add_argument("-f", "--function", required=True)
    parser.add_argument("-p", "--payload", required=False)

    args = parser.parse_args()
    act = args.action
    func = args.function
    pay = args.payload

    if act == 'create':
        create_lambda_function(func)

    elif act == 'invoke':
        invoke_lambda_function(func, pay)

    elif act == 'update':
        update_lambda_function(func)

    print("action finished!")
