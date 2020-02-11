## AWS Serverless Load Test for Aurora PostgreSQL

This basic serverless function applies simulated SELECT and INSERT load against an Amazon Aurora PostgreSQL database.  Successful executions are logged to Amazon Cloudwatch where statement duration can be viewed.

The components of this app are: 
1. A client-script (sqs_test_trigger.py) that the user executes to begin the test, adjust volume, and change host endpoints
2. An Amazon SQS queue that enques requests from this script
3. An Amazon Lambda function that picks up queue messages from SQS and makes DML calls to the Aurora endpoint.

Things to note about this implementation:
- This is not an industry standard benchmark
- Lambda does not scale it's SQS polling linerally or in real-time based on queue-depth. This means if you generate a high amount of SQS messages, your load against the database might come in bursts as lambda picks up new messages

This function was used in preparation for AWS re:Invent 2019 [FSI309](https://www.portal.reinvent.awsevents.com/connect/sessionDetail.ww?SESSION_ID=97951&csrftkn=622O-2731-X53I-IAF6-ALHH-B1IN-02QT-B9X4) - Relational databases: Performance, scale, and availability.


## Deployment

- For deployment of SQS and Lambda components, AWS CodePipeline is used in the way desribed here: https://docs.aws.amazon.com/lambda/latest/dg/build-pipeline.html
- You will need an S3 bucket for the cloudformation packaging, update the buildspec.yaml with your bucket name.
- For deployment of the Amazon Aurora database, that is not handled in this repo. Deploy and setup the database seperatly, then provide DBNAME & HOST information in the client-script sqs_test_trigger.py. The database tables/columns required are below.
- AWS Secrets Manager is used to store your database name and password. Setup a secret for the RDS username and password and update the paramaters.json file with the secret name.
- VPC is used to protect the database from public access. Place the RDS database into a VPC SecurityGroup(s) and Subnet(s) and update the parameters.json file to reflect which security groups and subnets the lambda function should use. In order to block inbound traffic, remove the internet gateway but create a NAT gateway and s3 VPC endpoint. Update route table accordingly.


Database DDL
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

Open sqs_test_trigger.py in an environment that has boto3 setup with access to the SQS queue. Update the fields to reflect your desired test and then execute the file in your local python env. I use AWS Cloud9 for this.


## License Summary

This sample code is made available under the MIT-0 license. See the LICENSE file.
