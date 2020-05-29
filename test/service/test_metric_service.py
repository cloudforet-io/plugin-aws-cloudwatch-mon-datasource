import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from spaceone.core.unittest.result import print_data
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core import utils
from spaceone.core.transaction import Transaction
from spaceone.monitoring.error import *
from spaceone.monitoring.connector.aws_boto_connector import AWSBotoConnector
from spaceone.monitoring.service.metric_service import MetricService
from spaceone.monitoring.info.metric_info import PluginMetricDataResponse, PluginMetricsResponse


class TestMetricService(unittest.TestCase):

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
    @patch.object(AWSBotoConnector, 'list_metrics')
    def test_list_metrics(self, mock_list_metrics, *args):
        mock_list_metrics.return_value = {
            'metrics': [
                {
                    'key': 'StatusCheckFailed_System',
                    'name': 'StatusCheckFailed_System',
                    'unit': {'x': 'Timestamp', 'y': 'Count'},
                    'chart_type': 'line',
                    'chart_options': {}
                }, {
                    'key': 'EBSReadOps',
                    'name': 'EBSReadOps',
                    'unit': {'x': 'Timestamp', 'y': 'Count'},
                    'chart_type': 'line',
                    'chart_options': {}
                }
            ]
        }

        params = {
            'options': {},
            'secret_data': {},
            'resource': 'arn:aws:ec2:ap-northeast-2:072548720675:instance/i-0547704161b1aa823'
        }

        self.transaction.method = 'list'
        metric_svc = MetricService(transaction=self.transaction)
        for response in metric_svc.list(params.copy()):
            print_data(response, 'test_list_metrics')
            PluginMetricsResponse(response)

    @patch.object(AWSBotoConnector, '__init__', return_value=None)
    @patch.object(AWSBotoConnector, 'create_session', return_value=None)
    @patch.object(AWSBotoConnector, 'get_metric_data')
    def test_get_metric_data(self, mock_get_metric_data, *args):
        end = datetime.utcnow()
        start = end - timedelta(days=1)
        mock_get_metric_data.return_value = {
            'labels': [
                {'seconds': 1586988300},
                {'seconds': 1586988000},
                {'seconds': 1586987700},
                {'seconds': 1586987400},
                {'seconds': 1586987100},
                {'seconds': 1586986800},
                {'seconds': 1586986500},
                {'seconds': 1586986200},
                {'seconds': 1586985900},
                {'seconds': 1586985600},
                {'seconds': 1586985300},
                {'seconds': 1586985000}
            ],
            'values': [4.0, 4.0, 4.0, 4.0, 4.4, 4.4, 4.0, 4.0, 6.0, 4.0, 4.0, 4.4]
        }

        params = {
            'options': {},
            'secret_data': {},
            'resource': 'arn:aws:ec2:ap-northeast-2:072548720675:instance/i-0547704161b1aa823',
            'metric': 'CPUUtilization',
            'start': start.isoformat(),
            'end': end.isoformat()
        }

        self.transaction.method = 'get_data'
        metric_svc = MetricService(transaction=self.transaction)
        for response in metric_svc.get_data(params.copy()):
            print_data(response, 'test_get_metric_data')
            PluginMetricDataResponse(response)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
