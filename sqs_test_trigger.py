import boto3

# Create SQS client
sqs = boto3.client('sqs')

queue_url = 'https://sqs.us-east-1.amazonaws.com/313021996969/PostgreTest'

# Send message to SQS queue

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
                'StringValue': '20'
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

for i in range(10):
    print(call_sqs('SELECT'))
    print(call_sqs('INSERT'))