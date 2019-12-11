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

import psycopg2
import os
import json
import random
import timeit
from test_object import TestConfig
from result_log import Log


def lambda_handler(event, context):

    test_config = TestConfig(event)
    response, elapsed = evaluate(test_config)
    return respond(response,elapsed,test_config)

def evaluate(test_config):
    
    if test_config.action == 'INSERT':
        start_time = timeit.default_timer()
        response = (None, insert(test_config.dmls, test_config.dbname, test_config.user, test_config.passw, test_config.host))
        elapsed = timeit.default_timer() - start_time
        return response, elapsed
        
    elif test_config.action == 'SELECT':
        start_time = timeit.default_timer()
        response = (None, select(test_config.dmls, test_config.dbname, test_config.user, test_config.passw, test_config.host))
        elapsed = timeit.default_timer() - start_time
        return response, elapsed
        
    else:
        return ValueError('Unsupported event "{}"'.format(test_config.action))


def insert(dmls, dbname, user, passw, host):
    try:
        conn = psycopg2.connect("dbname=" + dbname + ' user=' + user +' password=' + passw + ' host=' + host)
        cur = conn.cursor()
        for dml in range(dmls):
            cur.execute("INSERT INTO transactions (type, date, quantity, price) VALUES (%s, %s, %s, %s)",(random.randint(1,10), '2019-01-0' + str(random.randint(1,9)), random.randint(1,1000), round(random.uniform(0,500),2)))
        conn.commit()
        cur.close()
        conn.close()
        print ('inserts complete')
    except psycopg2.Error as e:
        print (e)
        

def select(dmls, dbname, user, passw, host):
    try:
        conn = psycopg2.connect("dbname=" + dbname + ' user=' + user +' password=' + passw + ' host=' + host)
        cur = conn.cursor()
        for dml in range(dmls):
            cur.execute("SELECT type.name, sum(transactions.quantity) FROM type INNER JOIN transactions on type.id = transactions.type GROUP BY type.name")
        cur.close()
        conn.close()
        #rows = cur.fetchall()
        #for row in rows:
        #    print (row)
        print ('selects complete')
    except psycopg2.Error as e:
        print (e)
    
    
#def respond(err, res=None, test_config):
def respond(response, elapsed, test_config):
    Log(elapsed, test_config.dbname, test_config.action)
    return {
        'statusCode': '400' if response.err else '200',
        'body': response.err.message if response.err else json.dumps(response.res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


