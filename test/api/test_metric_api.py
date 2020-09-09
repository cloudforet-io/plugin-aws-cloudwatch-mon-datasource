import unittest
from unittest.mock import patch
from google.protobuf.empty_pb2 import Empty

from spaceone.core.unittest.result import print_message
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core import utils
from spaceone.core.service import BaseService
from spaceone.core.locator import Locator
from spaceone.core.pygrpc import BaseAPI
from spaceone.api.monitoring.plugin import metric_pb2
from spaceone.monitoring.api.plugin.metric import Metric
from test.factory.metric_factory import MetricsResponseFactory, MetricDataResponseFactory


class _MockMetricService(BaseService):

    def list(self, params):
        return MetricsResponseFactory()

    def get_data(self, params):
        return MetricDataResponseFactory()


class TestMetricAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.monitoring')
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    @patch.object(BaseAPI, '__init__', return_value=None)
    @patch.object(Locator, 'get_service', return_value=_MockMetricService())
    @patch.object(BaseAPI, 'parse_request')
    def test_list_metrics(self, mock_parse_request, *args):
        params = {}
        mock_parse_request.return_value = (params, {})

        metric_servicer = Metric()
        response = metric_servicer.list({}, {})

        print_message(response, 'test_list_metrics')
        self.assertIsInstance(response, metric_pb2.PluginMetricsResponse)

    @patch.object(BaseAPI, '__init__', return_value=None)
    @patch.object(Locator, 'get_service', return_value=_MockMetricService())
    @patch.object(BaseAPI, 'parse_request')
    def test_get_metric_data(self, mock_parse_request, *args):
        params = {}
        mock_parse_request.return_value = (params, {})

        metric_servicer = Metric()
        response = metric_servicer.get_data({}, {})
        print_message(response, 'test_get_metric_data')
        self.assertIsInstance(response, metric_pb2.PluginMetricDataResponse)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
