import logging
import boto3
import time
from datetime import datetime, timedelta

from spaceone.core import utils
from spaceone.monitoring.error import *

__all__ = ['CloudWatch']

_LOGGER = logging.getLogger(__name__)


class CloudWatch(object):

    def __init__(self, session):
        self.session = session
        self.client = self.session.client('cloudwatch')

    def list_metrics(self, namespace, dimensions):
        paginator = self.client.get_paginator('list_metrics')

        responses = paginator.paginate(Namespace=namespace, Dimensions=dimensions)

        metrics_info = []

        for response in responses:
            for metric in response['Metrics']:
                metric_name = metric['MetricName']
                unit = self._get_metric_unit(namespace, dimensions, metric_name)
                chart_type, chart_option = self._get_chart_info(namespace, dimensions, metric_name)

                metric_info = {
                    'key': metric_name,
                    'name': metric_name,
                    'unit': unit,
                    'chart_type': chart_type,
                    'chart_options': chart_option
                }

                metrics_info.append(metric_info)

        return {
            'metrics': metrics_info
        }

    def get_metric_data(self, namespace, dimensions, metric_name, start, end, period, stat, limit=None):
        metric_id = f'metric_{utils.random_string()[:12]}'

        extra_opts = {}

        if limit:
            extra_opts['MaxDatapoints'] = limit

        response = self.client.get_metric_data(
            MetricDataQueries=[{
                'Id': metric_id,
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metric_name,
                        'Dimensions': dimensions
                    },
                    'Period': period,
                    'Stat': stat
                }
            }],
            StartTime=start,
            EndTime=end,
            ScanBy='TimestampAscending',
            **extra_opts
        )

        metric_data_info = {
            'labels': [],
            'values': []
        }

        for metric_data in response.get('MetricDataResults', []):
            metric_data_info['labels'] = list(map(self._convert_timestamp, metric_data['Timestamps']))
            metric_data_info['values'] += metric_data['Values']

        return metric_data_info

    @staticmethod
    def _convert_timestamp(metric_datetime):
        return utils.datetime_to_iso8601(metric_datetime)

    def _get_metric_unit(self, namespace, dimensions, metric_name):
        end = datetime.utcnow()
        start = end - timedelta(minutes=60)

        response = self.client.get_metric_statistics(
            Namespace=namespace,
            Dimensions=dimensions,
            MetricName=metric_name,
            StartTime=start,
            EndTime=end,
            Period=600,
            Statistics=['SampleCount']
        )

        return_dict = {
            'x': 'Timestamp',
            'y': ''
        }

        for data_point in response.get('Datapoints', []):
            unit = data_point['Unit']

            if unit != 'None':
                return_dict['y'] = unit
                return return_dict

        return return_dict

    @staticmethod
    def _get_chart_info(namespace, dimensions, metric_name):
        return 'line', {}
