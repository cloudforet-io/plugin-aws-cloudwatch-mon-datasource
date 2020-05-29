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
        config.init_conf(service='monitoring')
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    @patch.object(AWSBotoConnector, '__init__', return_value=None)
    def test_parse_arn(self, *args):
        resource = 'arn:aws:ec2:us-east-1:123456789012:vpc/vpc-fd580e98'

        aws_mgr = AWSManager()
        aws_mgr._parse_arn(resource)

    @patch.object(AWSBotoConnector, '__init__', return_value=None)
    def test_get_cloudwatch_query(self, *args):
        resource = 'arn:aws:ec2:ap-northeast-2:072548720675:instance/i-0547704161b1aa823'

        aws_mgr = AWSManager()
        arn = aws_mgr._parse_arn(resource)
        namespace, dimensions = aws_mgr._get_cloudwatch_query(arn, resource)
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
