## AWS Serverless Load Test for Aurora PostgreSQL
This basic serverless function applies simulated SELECT and INSERT load against an Amazon Aurora PostgreSQL database.  Successful executions are logged to Amazon Cloudwatch where statement duration can be viewed.

The components of this app are: 
1. A client-script (sqs_test_trigger.py) that the user executes to begin the test, adjust volume, and change host endpoints
2. An Amazon SQS queue that enques requests from this script
3. An Amazon Lambda function that picks up queue messages from SQS and makes DML calls to the Aurora endpoint.
4. Custom CloudWatch metrics with elapsed time for each request.

Things to note about this implementation:
- This is not an industry standard benchmark
- Lambda does not scale it's SQS polling linerally or in real-time based on queue-depth. This means if you generate a high amount of SQS messages, your load against the database might come in bursts as lambda picks up new messages

This function was used in preparation for AWS re:Invent 2019 [FSI309](https://www.portal.reinvent.awsevents.com/connect/sessionDetail.ww?SESSION_ID=97951&csrftkn=622O-2731-X53I-IAF6-ALHH-B1IN-02QT-B9X4) - Relational databases: Performance, scale, and availability.


## License Summary
This sample code is made available under the MIT-0 license. See the LICENSE file.
Amazon Employees, see ticket V164744705 for open source approval.


## Deployment
1. Setup S3, VPC, Aurora, and Secrets:
    - Create a S3 bucket to store intermediate build files.
    - Setup the Amazon Aurora database you wish to test. If you want to use the tables in this example, see the table structure below.
    - Setup a VPC with a public and private subnet, S3 private endpoint, and NAT gateway.
    - Setup a Secret in AWS Secretes Manager for the username and password of the Aurora database.

2. Setup a CodePipeline following [this](https://docs.aws.amazon.com/lambda/latest/dg/build-pipeline.html) example. Then:
    - Add an environment variable to the Build stage called "BUCKET" with the value as your S3 bucket name created above.
    - Add 3 Parameter overrides in the Deploy stage for "SecretName", "SecurityGroups", and "Subnets". Example syntax:
    {"SecretName": "YourSecret", "SecurityGroups": "sg-yours", "Subnets":"subnet-yours1, subnet-yours2"}


Database DDL Setup:
| table_name | ordinal_position | column_default | is_nullable | data_type |
| --- | --- | --- | --- | --- |
| transactions |	1 |	nextval('transactions_id_seq'::regclass) |	NO |	integer |
|transactions |	2 |	NULL | YES |	integer |  
|transactions |	3	| NULL | YES |	date | 
|transactions |	4	| NULL | YES |	integer | 
|transactions |	5	| NULL | YES |	double precision |  
|type |	1 |	NULL |	YES |	integer |  
|type |	2 |	NULL |	YES |	text |  


## Execution
Open sqs_test_trigger.py in an environment that has boto3 setup with access to the SQS queue URL.

Update the following fields based on your target resources:
- "queue_url" should reflect the public SQS endpoint created by your pipeline
- "database_url" is the Aurora endpoint you wish to hit. Note that if you want SELECT statements to hit read-only and INSERT statements to hit the primary, you need to change the script to handle 2 database endpoints.
- "database_name" is the PostgreSQL database name you setup in Aurora

Alter the load variables as desired and then execute the python script to begin the test. Observe performance metrics in your RDS dashboard or put together a custom CloudWatch dashboard that shows SQS queue depth, lambda function executions, RDS metrics, and your custom metrics.


## TODO
- Everything in Deployment section under item #1 should be added to this library for automation.
- CodePipeline setup should be automated.
- Determine a mechanism that will scale Lambda linerally, in order to more directly control load on the database and not be subject to the batching and concurrency restrictions. This would likely replace SQS.
- Change the DDL and DML to a more robust and industry standard test.