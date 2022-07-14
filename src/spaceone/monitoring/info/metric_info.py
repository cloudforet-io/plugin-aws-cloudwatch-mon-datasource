from spaceone.api.monitoring.plugin import metric_pb2
from spaceone.core.pygrpc.message_type import *

__all__ = ['MetricsInfo', 'MetricDataInfo']


def MetricInfo(metric):
    info = {
        'key': metric['key'],
        'name': metric['name'],
        'metric_query': change_struct_type(metric['metric_query'])
    }

    if 'unit' in metric:
        info.update({'unit': change_struct_type(metric['unit'])})

    if 'group' in metric:
        info.update({'group': metric['group']})

    return metric_pb2.MetricInfo(**info)


def MetricsInfo(result):
    info = {
        'metrics': [MetricInfo(metric) for metric in result['metrics']]
    }

    return metric_pb2.MetricsInfo(**info)


def MetricDataInfo(metric_data):
    info = {
        'labels': change_list_value_type(metric_data.get('labels', [])),
        'values': change_struct_type(metric_data['values'])
    }

    return metric_pb2.MetricDataInfo(**info)
