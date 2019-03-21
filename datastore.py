import boto3
import os


session = boto3.session.Session()
client = session.client('s3',
                        region_name='sfo2',
                        endpoint_url='https://sfo2.digitaloceanspaces.com',
                        aws_access_key_id=os.environ.get('DATASTORE_KEY'),
                        aws_secret_access_key=os.environ.get('DATASTORE_SECRET'))
BUCKET_NAME = os.environ.get('BUCKET_NAME')


def put_object(origin, destination):
    with open(origin, 'rb') as f:
        response = client.put_object(Bucket=BUCKET_NAME, Key=destination, Body=f)

    return response
