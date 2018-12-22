import os

import boto3


class Aws(object):

    _session = None

    @classmethod
    def create_session(cls):
        if not cls._session:
            cls._session = boto3.session.Session(
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name='ap-northeast-1',
            )

        return cls._session

    @classmethod
    def get_codedeploy_client(cls):
        session = cls.create_session()
        return session.client('codedeploy')
