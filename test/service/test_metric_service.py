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
from spaceone.monitoring.info.metric_info import MetricsInfo, MetricDataInfo


class TestMetricService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.monitoring')
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
                    'metric_query': {
                        'Dimensions': [{'Name': 'HostedZoneId', 'Value': 'Z01028552THR4GSCEJ9E3'}],
                        'MetricName': 'DNSQueries',
                        'Namespace': 'AWS/Route53'
                    }
                }, {
                    'key': 'EBSReadOps',
                    'name': 'EBSReadOps',
                    'unit': {'x': 'Timestamp', 'y': 'Count'},
                    'metric_query': {
                        'Dimensions': [{'Name': 'HostedZoneId', 'Value': 'Z01028552THR4GSCEJ9E3'}],
                        'MetricName': 'DNSQueries',
                        'Namespace': 'AWS/Route53'
                    }
                }
            ]
        }

        params = {
            'options': {},
            'secret_data': {},
            'query': {
                "region_name": "ap-southeast-1",
                "metrics_info": [
                    {
                        "Namespace": "AWS/EC2",
                        "Dimensions": [
                            {
                                "Name": "InstanceId",
                                "Value": "i-0ecbd2feb6ae4ee65"
                            }
                        ]
                    },
                    {
                        "Dimensions": [
                            {
                                "Name": "InstanceId",
                                "Value": "i-0ecbd2feb6ae4ee65"
                            }
                        ],
                        "Namespace": "CWAgent"
                    }
                ]
            }
        }

        self.transaction.method = 'list'
        metric_svc = MetricService(transaction=self.transaction)
        response = metric_svc.list(params.copy())
        print_data(response, 'test_list_metrics')
        MetricsInfo(response)

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
            'resource': {
                "namespace": "AWS/EC2",
                "dimensions": [
                    {
                        "Name": "InstanceId",
                        "Value": "i-011e8d755568b446b"
                    }
                ],
                "region_name": "ap-northeast-2"
            },
            'metric': 'CPUUtilization',
            'start': start.isoformat(),
            'end': end.isoformat()
        }

        self.transaction.method = 'get_data'
        metric_svc = MetricService(transaction=self.transaction)
        response = metric_svc.get_data(params.copy())
        print_data(response, 'test_get_metric_data')
        MetricDataInfo(response)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
