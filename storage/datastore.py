from dotenv import load_dotenv
load_dotenv()
from abc import ABC, abstractmethod

import boto3
import os
import logging

log = logging.getLogger('app.datastore')


class DataStore(ABC):
    @abstractmethod
    def move_object(self, origin, destination):
        pass

    @abstractmethod
    def put_object(self, origin, destination):
        pass

    @abstractmethod
    def delete_object(self, origin):
        pass


class RemoteDataStore(DataStore):

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
        self.client.copy_object(Bucket=self.bucket_name, CopySource=origin, Key=destination)
        self.delete_object(origin)

    def delete_object(self, origin):
        self.client.delete_object(Bucket=self.bucket_name, Key=origin)


class LocalDataStore(DataStore):

    def put_object(self, origin, destination):
        with open(destination, 'wb') as f:
            f.write(origin.read())

    def move_object(self, origin, destination):
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        os.rename(origin, destination)

    def delete_object(self, origin):
        os.remove(origin)


TARGETS = {RemoteDataStore.__name__: RemoteDataStore(),
           LocalDataStore.__name__: LocalDataStore()}


class Storage(DataStore):

    def delete_object(self, origin):
        target = TARGETS[os.environ.get('DATASTORE_TARGET', LocalDataStore.__name__)]
        target.delete_object(origin)

    def put_object(self, origin, destination):
        target = TARGETS[os.environ.get('DATASTORE_TARGET', LocalDataStore.__name__)]
        target.put_object(origin, destination)

    def move_object(self, origin, destination):
        target = TARGETS[os.environ.get('DATASTORE_TARGET', LocalDataStore.__name__)]
        log.info("Moving object from %s to %s using service %s".format(origin, destination, target.__class__.__name__))

        target.move_object(origin, destination)

