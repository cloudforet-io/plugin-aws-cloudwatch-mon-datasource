from spaceone.api.monitoring.plugin import metric_pb2, metric_pb2_grpc
from spaceone.core.pygrpc import BaseAPI


class Metric(BaseAPI, metric_pb2_grpc.MetricServicer):

    pb2 = metric_pb2
    pb2_grpc = metric_pb2_grpc

    def list(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('MetricService', metadata) as metric_service:
            response_stream = metric_service.list(params)
            for response in response_stream:
                yield self.locator.get_info('PluginMetricsResponse', response)

    def get_data(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('MetricService', metadata) as metric_service:
            response_stream = metric_service.get_data(params)
            for response in response_stream:
                yield self.locator.get_info('PluginMetricDataResponse', response)
