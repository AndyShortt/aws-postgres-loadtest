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
            