import boto3
import os
import logging

log = logging.getLogger('app.datastore')


class RemoteDataStore:

    def __init__(self):
        log.info('Initializing remote datastore')
        session = boto3.session.Session()
        self.client = session.client(os.environ.get('DATASTORE_SERVICE_NAME', 's3'),
                                     region_name=os.environ.get('DATASTORE_REGION_NAME', 'sfo2'),
                                     endpoint_url=os.environ.get('DATASTORE_ENDPOINT_URL',
                                                                 'https://sfo2.digitaloceanspaces.com'),
                                     aws_access_key_id=os.environ.get('DATASTORE_KEY'),
                                     aws_secret_access_key=os.environ.get('DATASTORE_SECRET'))
        self.bucket_name = os.environ.get('BUCKET_NAME')

    def put_object(self, origin, destination):
        with open(origin, 'rb') as f:
            self.client.put_object(Bucket=self.bucket_name, Key=destination, Body=f)

    def move_object(self, origin, destination):
        self.put_object(origin, destination)
        os.remove(origin)


class LocalDataStore:
    def move_object(self, origin, destination):
        os.rename(origin, destination)


TARGETS = {RemoteDataStore.__name__: RemoteDataStore(),
           LocalDataStore.__name__: LocalDataStore()}


def move_object(origin, destination):
    target = TARGETS[os.environ.get('DATASTORE_TARGET', RemoteDataStore.__name__)]
    log.info("Moving object from %s to %s using service %s".format(origin, destination, target.__class__.__name__))

    target.move_object(origin, destination)
