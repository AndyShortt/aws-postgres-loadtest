# Copyright 2019-2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import os
import json
from secrets import Secrets

class TestConfig: 
    def __init__(self, record): 
        self.action = record['messageAttributes']['Action']['stringValue']
        self.dmls = int(record['messageAttributes']['DMLS']['stringValue'])
        self.dbname = record['messageAttributes']['DBNAME']['stringValue']
        secrets = Secrets(self.dbname)
        self.passw = secrets.secret_values['password']
        self.user = secrets.secret_values['username']
        self.host = record['messageAttributes']['HOST']['stringValue']