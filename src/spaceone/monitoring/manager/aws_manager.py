import logging
import time
from spaceone.core.manager import BaseManager
from spaceone.core.utils import get_dict_value
from spaceone.monitoring.connector.aws_boto_connector import AWSBotoConnector
from spaceone.monitoring.error import *
_LOGGER = logging.getLogger(__name__)

_STAT_MAP = {
    'AVERAGE': 'Average',
    'MAX': 'Maximum',
    'MIN': 'Minimum',
    'SUM': 'Sum'
}

# CW_AGENT_DEFAULT_NS = 'CWAgent'
DEFAULT_REGION = 'us-east-1'


class AWSManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aws_connector: AWSBotoConnector = self.locator.get_connector('AWSBotoConnector')

    def verify(self, schema, options, secret_data):
        self.aws_connector.create_session(schema, options, secret_data)

    def list_metrics(self, schema, options, secret_data, resource):
        secret_data['region_name'] = resource.get('region_code', DEFAULT_REGION)
        self.aws_connector.create_session(schema, options, secret_data)

        cloudwatch_info = self._get_cloudwatch_info(resource)

        metrics = []
        for namespace, dimension_info in cloudwatch_info.items():
            default_dimension = dimension_info.get('DEFAULT')
            results = self.aws_connector.list_metrics(namespace, default_dimension)
            metrics.extend(results.get('metrics', []))

        return {'metrics': metrics}

    def get_metric_data(self, schema, options, secret_data, resource, metric, start, end, period, stat):
        _LOGGER.debug(f'[get_metric_data] period: {period}')
        _LOGGER.debug(f'[get_metric_data] start: {start}')
        _LOGGER.debug(f'[get_metric_data] end: {end}')
        _LOGGER.debug(f'[get_metric_data] stat: {stat}')

        secret_data['region_name'] = resource.get('region_code', DEFAULT_REGION)

        if period is None:
            period = self._make_period_from_time_range(start, end)

        stat = self._convert_stat(stat)
        self.aws_connector.create_session(schema, options, secret_data)

        return self.aws_connector.get_metric_data(resource.get('resources', []), metric, start, end, period, stat)

    @staticmethod
    def _convert_stat(stat):
        if stat is None:
            stat = 'AVERAGE'

        if stat not in _STAT_MAP.keys():
            raise ERROR_NOT_SUPPORT_STAT(supported_stat=' | '.join(_STAT_MAP.keys()))

        return _STAT_MAP[stat]

    @staticmethod
    def _make_period_from_time_range(start, end):
        start_time = int(time.mktime(start.timetuple()))
        end_time = int(time.mktime(end.timetuple()))
        time_delta = end_time - start_time

        # Max 60 point in start and end time range
        if time_delta <= 60*60:         # ~ 1h
            return 60
        elif time_delta <= 60*60*6:     # 1h ~ 6h
            return 60*10
        elif time_delta <= 60*60*12:    # 6h ~ 12h
            return 60*20
        elif time_delta <= 60*60*24:    # 12h ~ 24h
            return 60*30
        elif time_delta <= 60*60*24*3:  # 1d ~ 2d
            return 60*60
        elif time_delta <= 60*60*24*7:  # 3d ~ 7d
            return 60*60*3
        elif time_delta <= 60*60*24*14:  # 1w ~ 2w
            return 60*60*6
        elif time_delta <= 60*60*24*14:  # 2w ~ 4w
            return 60*60*12
        else:                            # 4w ~
            return 60*60*24

    @staticmethod
    def _get_cloudwatch_query(resource):
        data = resource.get('data', {})
        cloud_watch = data.get('cloudwatch', {})
        return cloud_watch.get('namespace'), cloud_watch.get('dimensions')

    @staticmethod
    def _get_cloudwatch_info(resource):
        return get_dict_value(resource, 'data.cloudwatch')
