import logging

from spaceone.core.manager import BaseManager
from spaceone.monitoring.model.metric_response_model import MetricsResponseModel, MetricDataResponseModel

_LOGGER = logging.getLogger(__name__)


class MetricManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def make_metrics_response(metrics_info):
        response_model = MetricsResponseModel({
            'result': metrics_info
        })
        response_model.validate()
        return response_model.to_primitive()

    @staticmethod
    def make_metric_data_response(metric_data_info):
        response_model = MetricDataResponseModel({
            'result': metric_data_info
        })
        response_model.validate()
        return response_model.to_primitive()
