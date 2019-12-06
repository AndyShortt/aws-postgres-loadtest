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


def lambda_handler(event, context):
    
    attr_action = event['Records'][0]['messageAttributes']['Action']['stringValue']
    attr_dmls = int(event['Records'][0]['messageAttributes']['DMLS']['stringValue'])
    attr_pass = event['Records'][0]['messageAttributes']['PASS']['stringValue']
    attr_user = event['Records'][0]['messageAttributes']['USER']['stringValue']
    attr_host = event['Records'][0]['messageAttributes']['HOST']['stringValue']
    attr_dbname = event['Records'][0]['messageAttributes']['DBNAME']['stringValue']

    if attr_action == 'INSERT':
        return respond(None, insert(attr_dmls, attr_dbname, attr_user, attr_pass, attr_host))
        
    elif attr_action == 'SELECT':
        return respond(None, select(attr_dmls, attr_dbname, attr_user, attr_pass, attr_host))
        
    else:
        return respond(ValueError('Unsupported event "{}"'.format(attr_action)))
        
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

    
def timer(button):

    return
    
    
def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }