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
import time
import random
import timeit
from test_object import TestConfig
from result_log import Log


def lambda_handler(event, context):

    for record in event['Records']:
        test_config = TestConfig(record)
        
        if test_config.action == 'INSERT':
            return insert(test_config.dmls, test_config.dbname, test_config.user, test_config.passw, test_config.host)
        
        elif test_config.action == 'SELECT':
            return select(test_config.dmls, test_config.dbname, test_config.user, test_config.passw, test_config.host)
        
        elif test_config.action == 'SELECT2':
            return select2(test_config.dmls, test_config.dbname, test_config.user, test_config.passw, test_config.host) 
        
        else:
            return {
            'statusCode': '400',
            'body': 'Unsupported event "{}"'.format(test_config.action),
            'headers': {
                'Content-Type': 'application/json',
                },
            }


def insert(dmls, dbname, user, passw, host):
    try:
        conn = psycopg2.connect("dbname=" + dbname + ' user=' + user +' password=' + passw + ' host=' + host)
        cur = conn.cursor()
        for dml in range(dmls):
            start_time = timeit.default_timer()
            cur.execute("INSERT INTO transactions (type, date, quantity, price) VALUES (%s, %s, %s, %s)",(random.randint(1,10), '2019-01-0' + str(random.randint(1,9)), random.randint(1,1000), round(random.uniform(0,500),2)))
            elapsed = timeit.default_timer() - start_time
            Log().put_metric('DURATION','ACTION', 'INSERT', 'Milliseconds', elapsed * 1000, dbname)
            time.sleep(random.randint(0,2))
        conn.commit()
        cur.close()
        conn.close()
        return ('inserts complete')
    except psycopg2.Error as e:
        return (e)
        

def select(dmls, dbname, user, passw, host):
    try:
        conn = psycopg2.connect("dbname=" + dbname + ' user=' + user +' password=' + passw + ' host=' + host)
        cur = conn.cursor()
        for dml in range(dmls):
            start_time = timeit.default_timer()
            cur.execute("SELECT type.name, sum(transactions.quantity) FROM type INNER JOIN transactions on type.id = transactions.type GROUP BY type.name")
            elapsed = timeit.default_timer() - start_time
            Log().put_metric('DURATION','ACTION', 'SELECT', 'Milliseconds', elapsed * 1000, dbname)
            time.sleep(random.randint(0,2))
        cur.close()
        conn.close()
        #rows = cur.fetchall()
        #for row in rows:
        #    print (row)
        return ('selects complete')
    except psycopg2.Error as e:
        return (e)


def select2(dmls, dbname, user, passw, host):
    try:
        conn = psycopg2.connect("dbname=" + dbname + ' user=' + user +' password=' + passw + ' host=' + host)
        cur = conn.cursor()
        for dml in range(dmls):
            start_time = timeit.default_timer()
            cur.execute("SELECT * FROM transactions WHERE quantity > %s",[random.randint(10,100)])
            elapsed = timeit.default_timer() - start_time
            Log().put_metric('DURATION','ACTION', 'SELECT2', 'Milliseconds', elapsed * 1000, dbname)
            time.sleep(random.randint(0,2))
        cur.close()
        conn.close()
        #rows = cur.fetchall()
        #for row in rows:
        #    print (row)
        return ('selects complete')
    except psycopg2.Error as e:
        return (e)
    
def respond(response):
    return {
        'statusCode': '200',
        'body': json.dumps(response),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


