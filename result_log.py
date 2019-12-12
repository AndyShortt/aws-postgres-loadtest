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
    def __init__(self, duration, dbname, action): 
        cloudwatch = boto3.client('cloudwatch')
    
        cloudwatch.put_metric_data(
            MetricData=[
                {
                    'MetricName': 'DURATION',
                    'Dimensions': [
                        {
                            'Name': 'ACTION',
                            'Value': action
                        },
                    ],
                    'Unit': 'ms',
                    'Value': (duration * 1000)
                },
            ],
            Namespace='PERFORMANCE/AURORA/' + dbname
        )
 