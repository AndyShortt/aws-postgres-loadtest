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
from get_secrets import get_secrets
from test_object import TestConfig


def lambda_handler(event, context):

    response, elapsed = evaluate(TestConfig(event))
    return respond(response,elapsed)

def evaluate(test_config):
    
    if test_config.action == 'INSERT':
        start_time = timeit.default_timer()
        response = respond(None, insert(test_config.dmls, test_config.dbname, test_config.user, test_config.passw, test_config.host))
        elapsed = timeit.default_timer() - start_time
        return response, elapsed
        
    elif test_config.action == 'SELECT':
        start_time = timeit.default_timer()
        response = respond(None, select(test_config.dmls, test_config.dbname, test_config.user, test_config.passw, test_config.host))
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

    
def timer(press):
    return
    
    
def respond(err, res=None):
    log()
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


