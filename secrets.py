import boto3
import base64
import json
from botocore.exceptions import ClientError

class Secrets:
    def __init__(self, dbname): 
        secret_name = "aurora/" + dbname + "/admin"
        region_name = "us-east-1"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        
        if 'SecretString' in get_secret_value_response:
            self.secret_values = json.loads(get_secret_value_response['SecretString'])
        else:
            self.secret_values = json.loads(base64.b64decode(get_secret_value_response['SecretBinary']))
            