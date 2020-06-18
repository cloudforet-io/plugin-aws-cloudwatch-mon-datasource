from schematics.models import Model
from schematics.types import ListType, DictType, StringType
from schematics.types.compound import ModelType

__all__ = ['PluginVerifyResponseModel']

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


class ReferenceKeyModel(Model):
    resource_type = StringType(required=True, choices=_SUPPORTED_RESOURCE_TYPE)
    reference_key = StringType(required=True)


class PluginOptionsModel(Model):
    supported_resource_type = ListType(StringType, default=_SUPPORTED_RESOURCE_TYPE)
    supported_stat = ListType(StringType, default=_SUPPORTED_STAT)
    reference_keys = ListType(ModelType(ReferenceKeyModel), default=_REFERENCE_KEYS)


class PluginVerifyModel(Model):
    options = ModelType(PluginOptionsModel, default=PluginOptionsModel)


class PluginVerifyResponseModel(Model):
    resource_type = StringType(required=True, default='monitoring.DataSource')
    actions = ListType(DictType(StringType))
    result = ModelType(PluginVerifyModel, required=True, default=PluginVerifyModel)
