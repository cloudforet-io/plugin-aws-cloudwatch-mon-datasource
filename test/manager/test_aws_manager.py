import unittest
import time
from datetime import datetime, timedelta
from unittest.mock import patch

from spaceone.core.unittest.result import print_data
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core import utils
from spaceone.monitoring.error import *
from spaceone.monitoring.connector.aws_boto_connector import AWSBotoConnector
from spaceone.monitoring.manager.aws_manager import AWSManager


class TestMetricManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.monitoring')
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    @patch.object(AWSBotoConnector, '__init__', return_value=None)
    def test_get_cloudwatch_query(self, *args):
        resource = {
            "namespace": "AWS/EC2",
            "dimensions": [
                {
                    "Name": "InstanceId",
                    "Value": "i-011e8d755568b446b"
                }
            ],
            "region_name": "ap-northeast-2"
        }

        aws_mgr = AWSManager()
        namespace, dimensions = aws_mgr._get_cloudwatch_query(resource)
        print_data(namespace, 'test_get_cloudwatch_query.namespace')
        print_data(dimensions, 'test_get_cloudwatch_query.dimensions')

    @patch.object(AWSBotoConnector, '__init__', return_value=None)
    def test_convert_stat(self, *args):
        aws_mgr = AWSManager()
        stat = aws_mgr._convert_stat('AVERAGE')
        print_data(stat, 'test_convert_stat')

    @patch.object(AWSBotoConnector, '__init__', return_value=None)
    def test_convert_stat_with_invalid_stat(self, *args):
        aws_mgr = AWSManager()
        with self.assertRaises(ERROR_NOT_SUPPORT_STAT):
            aws_mgr._convert_stat('aver')

    @patch.object(AWSBotoConnector, '__init__', return_value=None)
    def test_make_period_from_time_range(self, *args):
        aws_mgr = AWSManager()

        end = datetime.utcnow()
        start = end - timedelta(days=1)

        period = aws_mgr._make_period_from_time_range(start, end)
        print_data(period, 'test_make_period_from_time_range')


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
