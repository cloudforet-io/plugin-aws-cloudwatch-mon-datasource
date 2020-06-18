import logging

from spaceone.core.service import *

from spaceone.monitoring.error import *
from spaceone.monitoring.manager.aws_manager import AWSManager
from spaceone.monitoring.manager.metric_manager import MetricManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@event_handler
class MetricService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aws_mgr: AWSManager = self.locator.get_manager('AWSManager')
        self.metric_mgr: MetricManager = self.locator.get_manager('MetricManager')

    @transaction
    @check_required(['options', 'secret_data', 'resource'])
    def list(self, params):
        """Get CloudWatch metrics with arn

        Args:
            params (dict): {
                'options': 'dict',
                'secret_data': 'dict',
                'resource': 'dict'
            }

        Returns:
            plugin_metrics_response (dict)
        """
        metrics_info = self.aws_mgr.list_metrics(params['options'], params['secret_data'], params['resource'])
        yield self.metric_mgr.make_metrics_response(metrics_info)

    @transaction
    @check_required(['options', 'secret_data', 'resource', 'start', 'end'])
    @change_timestamp_value(['start', 'end'], timestamp_format='iso8601')
    def get_data(self, params):
        """Get CloudWatch metric data with arn

        Args:
            params (dict): {
                'options': 'dict',
                'secret_data': 'dict',
                'resource': 'str',
                'metric': 'str',
                'start': 'timestamp',
                'end': 'timestamp',
                'period': 'int',
                'stat': 'str'
            }

        Returns:
            plugin_metric_data_response (dict)
        """
        metric_data_info = self.aws_mgr.get_metric_data(params['options'], params['secret_data'], params['resource'],
                                                        params['metric'], params['start'], params['end'],
                                                        params.get('period'), params.get('stat'))
        yield self.metric_mgr.make_metric_data_response(metric_data_info)
