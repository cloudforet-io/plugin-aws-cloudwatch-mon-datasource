import factory
import time
import random

from spaceone.core import utils


class MetricFactory(factory.DictFactory):

    key = factory.LazyAttribute(lambda o: utils.generate_id('metric'))
    name = factory.LazyAttribute(lambda o: utils.random_string())
    unit = {
        'x': 'Datetime',
        'y': 'Count'
    }
    chart_type = 'line'
    chart_option = {}


class MetricsFactory(factory.DictFactory):

    metrics = factory.List([
        factory.SubFactory(MetricFactory) for _ in range(5)
    ])


class MetricsResponseFactory(factory.DictFactory):

    resource_type = 'monitoring.Metric'
    actions = []
    result = factory.SubFactory(MetricsFactory)


class MetricDataFactory(factory.DictFactory):

    labels = factory.List([
        int(time.time()) for _ in range(10)
    ])
    values = [random.randint(0, 20) for _ in range(10)]


class MetricDataResponseFactory(factory.DictFactory):

    resource_type = 'monitoring.Metric'
    actions = []
    result = factory.SubFactory(MetricDataFactory)