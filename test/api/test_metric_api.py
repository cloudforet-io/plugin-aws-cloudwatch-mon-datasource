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
            'query': {
                'region_name': 'us-east-1',
                "metrics_info": [
                    {
                        "Namespace": "AWS/EC2",
                        "Dimensions": [
                            {
                                "Name": "InstanceId",
                                "Value": "i-0f6720ba34f56ea15"
                            }
                        ]
                    },
                    {
                        "Dimensions": [
                            {
                                "Name": "InstanceId",
                                "Value": "i-0f6720ba34f56ea15"
                            }
                        ],
                        "Namespace": "CWAgent"
                    }
                ]
            }

        }

        response = self.monitoring.Metric.list(params)
        print_json(response)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
