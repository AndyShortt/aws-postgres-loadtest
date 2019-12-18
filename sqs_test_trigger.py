# Copyright 2017-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

import boto3
import time
import random

# Create SQS client
sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/313021996969/LambdaLoadTest-MySqsQueue-1UXEKC30XAJT6'

### ADD OR REDUCE LOAD HERE
load_wait = 0 # Seconds between batches
sqs_batch = 1 # size of SQS batch
total_duration = 1 # Total seconds to run test
dml_batch = 1 # for each sqs msg, how many DMLs to perform
###

# Define msg
def call_sqs(action, host):
    return sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=1,
        MessageAttributes={
            'Action': {
                'DataType': 'String',
                'StringValue': action
            },
            'DMLS': {
                'DataType': 'Number',
                'StringValue': str(dml_batch)
            },
            'HOST': {
                'DataType': 'String',
                'StringValue': host
            },
            'DBNAME': {
                'DataType': 'String',
                'StringValue': 'reinvent'
            }
        },
        MessageBody=(
            'Test PostgreSQL reinvent database SELECT statment times'
        )
    )


#Send msg
seconds = 0
while total_duration > seconds:
    for i in range(sqs_batch):
        print(call_sqs('SELECT','reinvent-serverless.cluster-cfsiasvduu7p.us-east-1.rds.amazonaws.com'))
        print(call_sqs('INSERT','reinvent-serverless.cluster-cfsiasvduu7p.us-east-1.rds.amazonaws.com'))
        print(call_sqs('SELECT2', 'reinvent-serverless.cluster-cfsiasvduu7p.us-east-1.rds.amazonaws.com'))
    time.sleep(load_wait - random.randint(0,1))
    seconds += load_wait
    
    #serverless
    # reinvent-serverless.cluster-cfsiasvduu7p.us-east-1.rds.amazonaws.com
    
    #provisioned
    #reinvent-test.cluster-ro-cfsiasvduu7p.us-east-1.rds.amazonaws.com
    #reinvent-test.cluster-cfsiasvduu7p.us-east-1.rds.amazonaws.com
    