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
    group = 'xxx'
    metric_query = {
        'region_name': 'us-east-1',
        'metrics_info': [
            {
                "Dimensions": [
                    {
                        "Name": "InstanceId",
                        "Value": "i-xxxxxx"
                    }
                ],
                "Namespace": "AWS/EC2"
            },
            {
                "Dimensions": [
                    {
                        "Name": "InstanceId",
                        "Value": "i-xxxxxx"
                    }
                ],
                "Namespace": "CWAgent"
            }
        ]
    }


class MetricsResponseFactory(factory.DictFactory):
    metrics = factory.List([
        factory.SubFactory(MetricFactory) for _ in range(5)
    ])


class MetricDataResponseFactory(factory.DictFactory):

    labels = factory.List([
        int(time.time()) for _ in range(10)
    ])
    values = [random.randint(0, 20) for _ in range(10)]

