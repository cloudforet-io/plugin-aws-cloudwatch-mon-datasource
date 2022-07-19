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

    def list_metrics(self, params):
        paginator = self.client.get_paginator('list_metrics')
        responses = paginator.paginate(**params)

        metrics_info = []
        for response in responses:
            for metric in response['Metrics']:
                metric_name = metric['MetricName']
                unit = self._get_metric_unit(params, metric_name)
                metric_key = metric_name
                # metric_key = self._set_metric_key(params['Namespace'], metric_name)

                metric_info = {
                    'key': metric_key,
                    'name': metric_name,
                    'unit': unit,
                    'group': params['Namespace'],
                    'metric_query': metric
                }

                metrics_info.append(metric_info)

        return {'metrics': metrics_info}

    def get_metric_data(self, metric_query, metric_name, start, end, period, stat, limit=None):
        extra_opts = {}

        if limit:
            extra_opts['MaxDatapoints'] = limit

        metric_dt_query = self._generate_get_data_param_query(metric_query, period, stat)

        response = self.client.get_metric_data(
            MetricDataQueries=metric_dt_query,
            StartTime=start,
            EndTime=end,
            ScanBy='TimestampAscending',
            **extra_opts
        )

        metric_data_info = {
            'labels': [],
            'values': {}
        }

        for metric_data in response.get('MetricDataResults', []):
            cloud_service_id = metric_data['Id'].replace('_', '-')

            if not metric_data_info.get('labels'):
                metric_data_info['labels'] = list(map(self._convert_timestamp, metric_data['Timestamps']))

            metric_data_info['values'].update({cloud_service_id: metric_data.get('Values', [])})

        return metric_data_info

    @staticmethod
    def _set_metric_key(namespace, metric_name):
        return f'{namespace}.{metric_name}'

    @staticmethod
    def _convert_timestamp(metric_datetime):
        return utils.datetime_to_iso8601(metric_datetime)

    def _get_metric_unit(self, params, metric_name):
        end = datetime.utcnow()
        start = end - timedelta(minutes=60)

        params.update({
            'MetricName': metric_name,
            'StartTime': start,
            'EndTime': end,
            'Period': 600,
            'Statistics': ['SampleCount']
        })

        response = self.client.get_metric_statistics(**params)

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
    def _generate_get_data_param_query(metric_query, period, stat):
        params = []

        for cloud_service_id, _metric in metric_query.items():
            if 'region_name' in _metric:
                del _metric['region_name']

            params.append({
                'Id': cloud_service_id.replace('-', '_'),
                'MetricStat': {
                    'Metric': _metric,
                    'Period': period,
                    'Stat': stat
                }
            })

        return params

    @staticmethod
    def _get_metric_namespace(metric_name):
        _metric_info = metric_name.split('.')

        if len(_metric_info) > 1:
            return _metric_info[0], _metric_info[1]
        else:
            return '', _metric_info[0]
