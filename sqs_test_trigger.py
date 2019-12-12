import boto3
import time
import random

# Create SQS client
sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/313021996969/PostgreTest'

### ADD OR REDUCE LOAD HERE
load_wait = 1 # Seconds between batches
sqs_batch = 10 # size of SQS batch
total_duration = 600 # Total seconds to run test
dml_batch = 10 # for each sqs msg, how many DMLs to perform
###

# Define msg
def call_sqs(action):
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
                'StringValue': 'reinvent-test.cluster-cfsiasvduu7p.us-east-1.rds.amazonaws.com'
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
        print(call_sqs('SELECT'))
        print(call_sqs('INSERT'))
        print(call_sqs('SELECT2'))
    time.sleep(load_wait - random.randint(0,1))
    seconds += load_wait