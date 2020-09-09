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
from spaceone.api.monitoring.plugin import data_source_pb2
from spaceone.monitoring.api.plugin.data_source import DataSource
from test.factory.data_source_factory import PluginVerifyResponseFactory


class _MockDataSourceService(BaseService):

    def verify(self, params):
        yield PluginVerifyResponseFactory()


class TestDataSourceAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.monitoring')
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    @patch.object(BaseAPI, '__init__', return_value=None)
    @patch.object(Locator, 'get_service', return_value=_MockDataSourceService())
    @patch.object(BaseAPI, 'parse_request')
    def test_verify_data_source(self, mock_parse_request, *args):
        params = {}
        mock_parse_request.return_value = (params, {})

        data_source_servicer = DataSource()
        response = data_source_servicer.verify({}, {})
        print_message(response, 'test_verify_data_source')


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
