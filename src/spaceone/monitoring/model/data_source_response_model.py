from schematics.models import Model
from schematics.types import ListType, DictType, StringType
from schematics.types.compound import ModelType

__all__ = ['PluginInitResponse']

_SUPPORTED_STAT = [
    'AVERAGE',
    'MAX',
    'MIN',
    'SUM'
]

_REQUIRED_KEYS = ['data.cloudwatch']
_REQUIRED_PROVIDERS = ['aws']


class PluginMetadata(Model):
    supported_stat = ListType(StringType, default=_SUPPORTED_STAT)
    required_keys = ListType(StringType, default=_REQUIRED_KEYS)
    supported_providers = ListType(StringType, default=_REQUIRED_PROVIDERS)


class PluginInitResponse(Model):
    _metadata = ModelType(PluginMetadata, default=PluginMetadata, serialized_name='metadata')
