# Copyright 2019-2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

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
 