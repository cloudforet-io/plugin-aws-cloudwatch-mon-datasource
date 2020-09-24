import functools
from spaceone.api.monitoring.plugin import metric_pb2
from spaceone.api.core.v1 import plugin_pb2
from spaceone.core.pygrpc.message_type import *

__all__ = ['PluginMetricsResponse', 'PluginMetricDataResponse']


def PluginAction(action):
    info = {
        'method': action['method'],
    }

    if 'options' in action:
        info['options'] = change_struct_type(action['options'])

    return plugin_pb2.PluginAction(**info)


def MetricInfo(metric):
    info = {
        'key': metric['key'],
        'name': metric['name'],
        'unit': change_struct_type(metric['unit']),
        'chart_type': metric['chart_type']
    }

    if 'chart_options' in metric:
        info.update({
            'chart_options': change_struct_type(metric['chart_options'])
        })

    return metric_pb2.MetricInfo(**info)


def MetricsInfo(result):
    info = {
        'metrics': [MetricInfo(metric) for metric in result['metrics']]
    }

    return metric_pb2.MetricsInfo(**info)


def PluginMetricsResponse(response):
    info = {
        'resource_type': response['resource_type'],
        'result': MetricsInfo(response['result'])
    }

    if response.get('actions'):
        info['actions']: [PluginAction(action) for action in response.get('actions', [])]

    return metric_pb2.PluginMetricsResponse(**info)


def MetricDataInfo(result):
    info = {
        'labels': change_list_value_type(result['labels']),
        'values': change_list_value_type(result['values'])
    }

    return metric_pb2.MetricDataInfo(**info)


def PluginMetricDataResponse(response):
    info = {
        'resource_type': response['resource_type'],
        'result': MetricDataInfo(response['result'])
    }

    if response.get('actions'):
        info['actions']: [PluginAction(action) for action in response.get('actions', [])]

    return metric_pb2.PluginMetricDataResponse(**info)
