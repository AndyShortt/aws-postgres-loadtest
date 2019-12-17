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
    def __init__(self, record): 
        action = record['messageAttributes']['Action']['stringValue']
        dmls = int(record['messageAttributes']['DMLS']['stringValue'])
        dbname = record['messageAttributes']['DBNAME']['stringValue']
        passw = get_secrets(dbname)['password']
        user = get_secrets(dbname)['username']
        host = record['messageAttributes']['HOST']['stringValue']