from spaceone.api.monitoring.plugin import log_pb2, log_pb2_grpc
from spaceone.core.pygrpc import BaseAPI


class Log(BaseAPI, log_pb2_grpc.LogServicer):

    pb2 = log_pb2
    pb2_grpc = log_pb2_grpc
