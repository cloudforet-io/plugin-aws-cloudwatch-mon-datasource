import unittest
import time
from unittest.mock import patch

from spaceone.core.unittest.result import print_data
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core import utils
from spaceone.core.transaction import Transaction
from spaceone.monitoring.error import *
from spaceone.monitoring.connector.aws_boto_connector import AWSBotoConnector
from spaceone.monitoring.service.data_source_service import DataSourceService
from spaceone.monitoring.info.data_source_info import PluginVerifyResponse


class TestDataSourceService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(service='monitoring')
        cls.transaction = Transaction({
            'service': 'monitoring',
            'api_class': 'DataSource'
        })
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    @patch.object(AWSBotoConnector, '__init__', return_value=None)
    @patch.object(AWSBotoConnector, 'create_session', return_value=None)
    def test_verify_data_source(self, *args):
        params = {
            'options': {},
            'secret_data': {}
        }

        self.transaction.method = 'verify'
        data_source_svc = DataSourceService(transaction=self.transaction)
        for response in data_source_svc.verify(params.copy()):
            print_data(response, 'test_verify_data_source')
            PluginVerifyResponse(response)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
