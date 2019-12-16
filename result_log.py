# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License. 

import json
import boto3

class Log: 
    def __init__(self): 
        self.cloudwatch = boto3.client('cloudwatch')
    
    def put_metric(self, name, dimension_name, dimension_value, unit, value, namespace):
        self.cloudwatch.put_metric_data(
            MetricData=[
                {
                    'MetricName': name,
                    'Dimensions': [
                        {
                            'Name': dimension_name,
                            'Value': dimension_value
                        },
                    ],
                    'Unit': unit,
                    'Value': value
                },
                {
                    'MetricName': 'COMPLETIONS',
                    'Dimensions': [
                        {
                           'Name':  dimension_name,
                           'Value':  dimension_value
                        },  
                    ],
                    'Unit': 'Count',
                    'Value': 1
                }
            ],
            Namespace='PERFORMANCE/AURORA/' + namespace
        )
 