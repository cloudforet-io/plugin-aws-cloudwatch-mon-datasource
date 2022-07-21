import logging
import time
from spaceone.core.manager import BaseManager
from spaceone.monitoring.connector.aws_boto_connector import AWSBotoConnector
from spaceone.monitoring.error import *
_LOGGER = logging.getLogger(__name__)

_STAT_MAP = {
    'AVERAGE': 'Average',
    'MAX': 'Maximum',
    'MIN': 'Minimum',
    'SUM': 'Sum'
}

DEFAULT_REGION = 'us-east-1'


class AWSManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aws_connector: AWSBotoConnector = self.locator.get_connector('AWSBotoConnector')

    def verify(self, schema, options, secret_data):
        self.aws_connector.create_session(schema, options, secret_data)

    def list_metrics(self, schema, options, secret_data, query):
        secret_data['region_name'] = query.get('region_name', DEFAULT_REGION)
        self.aws_connector.create_session(schema, options, secret_data)

        metrics = []
        for metric_info in query.get('metrics_info', []):
            if metric_info.get('Namespace') and metric_info.get('Dimensions'):
                results = self.aws_connector.list_metrics(metric_info)
                metrics.extend(results.get('metrics', []))

        return {'metrics': metrics}

    def get_metric_data(self, schema, options, secret_data, metric_query, metric, start, end, period, stat):
        secret_data['region_name'] = self.get_region_from_metric_query(metric_query)

        if period is None:
            period = self._make_period_from_time_range(start, end)

        stat = self._convert_stat(stat)
        self.aws_connector.create_session(schema, options, secret_data)

        return self.aws_connector.get_metric_data(metric_query, metric, start, end, period, stat)

    @staticmethod
    def get_region_from_metric_query(metric_query):
        for _query in metric_query.values():
            if 'region_name' in _query and _query['region_name'].lower() != 'global':
                return _query['region_name']

        return DEFAULT_REGION

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
