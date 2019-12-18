## AWS Serverless Load Test for Auora PostgreSQL

This basic serverless app applies simulated SELECT and INSERT load against an Amazon Aurora PostgreSQL database.  Successful executions are logged to Amazon Cloudwatch where statement duration can be viewed.

The components of this app are: 
1. A client-script (sqs_test_trigger.py) that the user executes to begin the test, adjust volume, and change host endpoints
2. An Amazon SQS queue that enques requests from this script
3. An Amazon Lambda function that picks up queue messages from SQS and makes DML calls to the Aurora endpoint.

Things to note about this implementation:
- This is not an industry standard benchmark
- Lambda does not scale it's SQS polling linerally or in real-time based on queue-depth. This means if you generate a high amount of SQS messages, your load against the database might come in bursts as lambda picks up new messages

## Deployment

- For deployment of SQS and Lambda components, AWS CodePipeline is used in the way desribed here: https://docs.aws.amazon.com/lambda/latest/dg/build-pipeline.html
- For deplotment of the Amazon Aurora database, that is not handled in this repo. Deploy and setup the database seperatly, then provide DBNAME & HOST information in the client-script.
- For storing database secrets in Amazon Secrets Manager, that is not handled in this repo. Setup database username and password seperatly.
- For creation of VPC, security group, and subnets, that is not handled in this repo. Setup those items then update the template.yaml to reflect.

## Execution

Open sqs_test_trigger.py in an environment that has boto3 setup with access to the SQS queue. Update the fields to reflect your desired test and then execute the file in your local python env. I use AWS Cloud9 for this.


## License Summary

This sample code is made available under the MIT-0 license. See the LICENSE file.