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

    def get_metric_data(self, resources, metric_name, start, end, period, stat, limit=None):
        extra_opts = {}

        if limit:
            extra_opts['MaxDatapoints'] = limit

        metric_dt_query = self._generate_get_data_param_query(resources, metric_name, period, stat)

        response = self.client.get_metric_data(
            MetricDataQueries=metric_dt_query,
            StartTime=start,
            EndTime=end,
            ScanBy='TimestampAscending',
            **extra_opts
        )

        metric_data_info = {
            'labels': [],
            'resource_values': {}
        }

        for metric_data in response.get('MetricDataResults', []):
            resource_id = resources[0].get('resource_id') if len(resources) == 1 else self._get_resource_id(resources, metric_data.get('Label'))

            if not metric_data_info.get('labels'):
                metric_data_info['labels'] = list(map(self._convert_timestamp, metric_data['Timestamps']))

            if resource_id is not None:
                metric_data_info['resource_values'].update({resource_id: metric_data.get('Values', [])})

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

    @staticmethod
    def _get_resource_id(resources, instance_id):
        resource_id = None

        for resource in resources:
            dimensions = resource.get('dimensions', [])

            for dimension in dimensions:
                if dimension.get('Value') == instance_id:
                    resource_id = resource.get('resource_id')

            if resource_id is not None:
                break

        return resource_id

    @staticmethod
    def _generate_get_data_param_query(resources, metric_name, period, stat):
        params = []
        for resource in resources:
            metric_id = f'metric_{utils.random_string()[:12]}'
            params.append({
                'Id': metric_id,
                'MetricStat': {
                    'Metric': {
                        'Namespace': resource.get('namespace'),
                        'MetricName': metric_name,
                        'Dimensions': resource.get('dimensions')
                    },
                    'Period': period,
                    'Stat': stat
                }
            })

        return params