import logging
import boto3

from spaceone.core import utils
from spaceone.core.connector import BaseConnector
from spaceone.monitoring.error import *
from spaceone.monitoring.connector.aws_boto_connector.cloud_watch import CloudWatch

__all__ = ['AWSBotoConnector']

_LOGGER = logging.getLogger(__name__)


class AWSBotoConnector(BaseConnector):

    def __init__(self, transaction, config):
        super().__init__(transaction, config)

    def create_session(self, options: dict, secret_data: dict):
        self._check_secret_data(secret_data)

        aws_access_key_id = secret_data['aws_access_key_id']
        aws_secret_access_key = secret_data['aws_secret_access_key']
        region_name = secret_data.get('region_name')
        role_arn = secret_data.get('role_arn')

        try:
            if role_arn:
                self._create_session_with_assume_role(aws_access_key_id, aws_secret_access_key, region_name, role_arn)
            else:
                self._create_session_with_access_key(aws_access_key_id, aws_secret_access_key, region_name)
        except Exception as e:
            raise ERROR_INVALID_CREDENTIALS()

    @staticmethod
    def _check_secret_data(secret_data):
        if 'aws_access_key_id' not in secret_data:
            raise ERROR_REQUIRED_PARAMETER(key='secret.aws_access_key_id')

        if 'aws_secret_access_key' not in secret_data:
            raise ERROR_REQUIRED_PARAMETER(key='secret.aws_secret_access_key')

    def _create_session_with_access_key(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.session = boto3.Session(aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key,
                                     region_name=region_name)

        sts = self.session.client('sts')
        sts.get_caller_identity()

    def _create_session_with_assume_role(self, aws_access_key_id, aws_secret_access_key, region_name, role_arn):
        self._create_session_with_access_key(aws_access_key_id, aws_secret_access_key, region_name)

        sts = self.session.client('sts')
        assume_role_object = sts.assume_role(RoleArn=role_arn, RoleSessionName=utils.generate_id('AssumeRoleSession'))
        credentials = assume_role_object['Credentials']

        self.session = boto3.Session(aws_access_key_id=credentials['AccessKeyId'],
                                     aws_secret_access_key=credentials['SecretAccessKey'],
                                     region_name=region_name,
                                     aws_session_token=credentials['SessionToken'])

    def list_metrics(self, *args, **kwargs):
        cw = CloudWatch(self.session)
        return cw.list_metrics(*args, **kwargs)

    def get_metric_data(self, *args, **kwargs):
        cw = CloudWatch(self.session)
        return cw.get_metric_data(*args, **kwargs)
