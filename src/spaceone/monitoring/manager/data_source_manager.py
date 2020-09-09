import logging

from spaceone.core.manager import BaseManager
from spaceone.monitoring.model.data_source_response_model import PluginInitResponse

_LOGGER = logging.getLogger(__name__)


class DataSourceManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def init_response():
        response_model = PluginInitResponse()
        response_model.validate()
        return response_model.to_primitive()
