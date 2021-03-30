from schematics.models import Model
from schematics.types import ListType, DictType, StringType
from schematics.types.compound import ModelType

__all__ = ['PluginInitResponse']

_SUPPORTED_RESOURCE_TYPE = [
    'inventory.Server',
    'inventory.CloudService'
]
_SUPPORTED_STAT = [
    'AVERAGE',
    'MAX',
    'MIN',
    'SUM'
]

_REFERENCE_KEYS = [
    {
      'resource_type': 'inventory.Server',
      'reference_key': 'data.cloudwatch'
    }, {
      'resource_type': 'inventory.CloudService',
      'reference_key': 'data.cloudwatch'
    }
]

_REQUIRED_KEYS = ['reference.resource_id']


class ReferenceKeyModel(Model):
    resource_type = StringType(required=True, choices=_SUPPORTED_RESOURCE_TYPE)
    reference_key = StringType(required=True)


class PluginMetadata(Model):
    supported_resource_type = ListType(StringType, default=_SUPPORTED_RESOURCE_TYPE)
    supported_stat = ListType(StringType, default=_SUPPORTED_STAT)
    required_keys = ListType(StringType, default=_REQUIRED_KEYS)


class PluginInitResponse(Model):
    _metadata = ModelType(PluginMetadata, default=PluginMetadata, serialized_name='metadata')
