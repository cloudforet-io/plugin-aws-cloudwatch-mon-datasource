import datetime
from spaceone.api.monitoring.plugin import metric_pb2
from spaceone.api.core.v1 import plugin_pb2
from spaceone.core.pygrpc.message_type import *
from spaceone.core import utils

__all__ = ['MetricsInfo', 'MetricDataInfo']


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


def MetricDataInfo(result):
    new_labels = []
    for label in result.get('labels', []):
        timestamp = label.get('seconds', 0)
        time = datetime.datetime.fromtimestamp(timestamp)
        new_labels.append(utils.datetime_to_iso8601(time))

    info = {
        'labels': change_list_value_type(new_labels),
        'values': change_list_value_type(result['values'])
    }

    return metric_pb2.MetricDataInfo(**info)