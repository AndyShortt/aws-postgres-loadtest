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

import os
import json
from get_secrets import get_secrets

class TestConfig: 
    def __init__(self, event): 
        self.action = event['Records'][0]['messageAttributes']['Action']['stringValue']
        self.dmls = int(event['Records'][0]['messageAttributes']['DMLS']['stringValue'])
        self.dbname = event['Records'][0]['messageAttributes']['DBNAME']['stringValue']
        self.passw = get_secrets(self.dbname)['password']
        self.user = get_secrets(self.dbname)['username']
        self.host = event['Records'][0]['messageAttributes']['HOST']['stringValue']