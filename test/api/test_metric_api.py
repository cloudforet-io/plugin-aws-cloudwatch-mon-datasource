import os
import unittest
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.tester import TestCase, print_json

AKI = os.environ.get('AWS_ACCESS_KEY_ID', None)
SAK = os.environ.get('AWS_SECRET_ACCESS_KEY', None)

if AKI == None or SAK == None:
    print("""
##################################################
# ERROR 
#
# Configure your AWS credential first for test
##################################################
example)

export AWS_ACCESS_KEY_ID=<YOUR_AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<YOUR_AWS_SECRET_ACCESS_KEY>

""")
    exit

class TestLog(TestCase):

    def test_init(self):
        v_info = self.monitoring.DataSource.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        schema = 'aws_access_key'
        options = {
        }
        secret_data = {
            'aws_access_key_id': AKI,
            'aws_secret_access_key': SAK
        }
        self.monitoring.DataSource.verify({'schema': schema, 'options': options, 'secret_data': secret_data})

    def test_metric_list(self):
        secret_data = {
            'aws_access_key_id': AKI,
            'aws_secret_access_key': SAK
        }

        params = {
            'options': {},
            'secret_data': secret_data,
            'schema': 'aws_access_key',
            'metric_query': {
                "cloud-svc-746e880efc54": {
                    "Namespace": "AWS/EC2",
                    "MetricName": "CPUUtilization",
                    "Dimensions": [
                        {
                            "Name": "InstanceId",
                            "Value": "i-09036be2a405bcxxxxx"
                        }
                    ],
                    "region_name": "ap-northeast-2"
                },
                "cloud-svc-fb341f730700": {
                    "Namespace": "AWS/EC2",
                    "MetricName": "CPUUtilization",
                    "Dimensions": [
                        {
                            "Name": "InstanceId",
                            "Value": "i-042786d33dfyyyyyy"
                        }
                    ],
                    "region_name": "ap-northeast-2"
                }
            },
            'metric': 'CPUUtilization',
            'start': "2022-07-12T13:25:40.437Z",
            'end': "2022-07-14T13:25:40.437Z"
        }

        response = self.monitoring.Metric.get_data(params)
        print_json(response)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
