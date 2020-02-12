# Copyright 2019-2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
import time
import random

sqs = boto3.client('sqs')

#### UPDATE TARGETS
queue_url = 'https://sqs.us-east-1.amazonaws.com/...YOUR-QUEUE...'
database_url = 'YOUR-RDS-ENDPOINT.us-east-1.rds.amazonaws.com'
database_name 'YOUR-AURORA-DATABASE-NAME'
###

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
                'StringValue': database_name
            }
        },
        MessageBody=(
            'Aurora DML execution request'
        )
    )


#Send msg
seconds = 0
while total_duration > seconds:
    for i in range(sqs_batch):
        print(call_sqs('SELECT',database_url))
        print(call_sqs('INSERT',database_url))
        print(call_sqs('SELECT2', database_url))
    time.sleep(max(load_wait,1) - random.randint(0,1))
    seconds += max(load_wait,1)
    