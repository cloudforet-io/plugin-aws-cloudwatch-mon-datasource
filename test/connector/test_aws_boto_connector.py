import unittest
import os
from datetime import datetime, timedelta
from unittest.mock import patch

from spaceone.core.unittest.result import print_data
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core import utils
from spaceone.core.transaction import Transaction
from spaceone.monitoring.manager.aws_manager import AWSManager
from spaceone.monitoring.connector.aws_boto_connector import AWSBotoConnector


class TestAWSBotoConnector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(service='monitoring')
        config_path = os.environ.get('TEST_CONFIG')
        test_config = utils.load_yaml_from_file(config_path)

        cls.aws_credentials = test_config.get('AWS_CREDENTIALS', {})
        cls.resource = test_config.get('RESOURCE')
        cls.metric = test_config.get('METRIC')

        cls.aws_connector = AWSBotoConnector(Transaction(), {})
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_create_session_with_aws_access_key(self):
        self.aws_connector.create_session({}, self.aws_credentials)

    def test_list_metrics(self):
        aws_mgr = AWSManager()
        arn = aws_mgr._parse_arn(self.resource)
        namespace, dimensions = aws_mgr._get_cloudwatch_query(arn, self.resource)

        self.aws_credentials['region_name'] = arn.region

        self.aws_connector.create_session({}, self.aws_credentials)
        metrics_info = self.aws_connector.list_metrics(namespace, dimensions)

        print_data(metrics_info, 'test_list_metrics')

    def test_get_metric_data(self):
        aws_mgr = AWSManager()
        arn = aws_mgr._parse_arn(self.resource)
        namespace, dimensions = aws_mgr._get_cloudwatch_query(arn, self.resource)

        self.aws_credentials['region_name'] = arn.region

        end = datetime.utcnow()
        start = end - timedelta(minutes=60)

        period = aws_mgr._make_period_from_time_range(start, end)
        stat = aws_mgr._convert_stat('AVERAGE')

        self.aws_connector.create_session({}, self.aws_credentials)
        metric_data_info = self.aws_connector.get_metric_data(namespace, dimensions, self.metric,
                                                              start, end, period, stat)

        print_data(metric_data_info, 'test_get_metric_data')

    def test_all_metric_data(self):
        aws_mgr = AWSManager()
        arn = aws_mgr._parse_arn(self.resource)
        namespace, dimensions = aws_mgr._get_cloudwatch_query(arn, self.resource)

        self.aws_credentials['region_name'] = arn.region

        end = datetime.utcnow()
        start = end - timedelta(minutes=60)

        period = aws_mgr._make_period_from_time_range(start, end)
        stat = aws_mgr._convert_stat('AVERAGE')

        self.aws_connector.create_session({}, self.aws_credentials)
        metrics_info = self.aws_connector.list_metrics(namespace, dimensions)

        for metric_info in metrics_info.get('metrics', []):
            metric_data_info = self.aws_connector.get_metric_data(namespace, dimensions, metric_info['key'],
                                                                  start, end, period, stat)

            print_data(metric_data_info, f'test_all_metric_data.{metric_info["key"]}')


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
