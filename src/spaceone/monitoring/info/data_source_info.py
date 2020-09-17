from spaceone.api.monitoring.plugin import data_source_pb2
from spaceone.api.core.v1 import plugin_pb2
from spaceone.core.pygrpc.message_type import *


__all__ = ['PluginInfo']


def PluginInfo(response):
    return data_source_pb2.PluginInfo(**response)
