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
import random

env_dmls = int(os.environ.get("DMLS"))
env_pass = os.environ.get("PASS")
env_user = os.environ.get("USER")
env_host = os.environ.get("HOST")
env_dbname = os.environ.get("DBNAME")

def lambda_handler(event, context):

    if event['Records'][0]['messageAttributes']['Action']['stringValue'] == 'INSERT':
        return respond(None, insert())
        
    elif event['Records'][0]['messageAttributes']['Action']['stringValue'] == 'SELECT':
        return respond(None, select())
        
    else:
        return respond(ValueError('Unsupported event "{}"'.format(event['Records'][0]['messageAttributes']['Action']['stringValue'])))
        
def insert():
    
    try:
        conn = psycopg2.connect("dbname=" + env_dbname + ' user=' + env_user +' password=' + env_pass + ' host=' + env_host)
        cur = conn.cursor()
        for dml in range(env_dmls):
            cur.execute("INSERT INTO transactions (type, date, quantity, price) VALUES (%s, %s, %s, %s)",(random.randint(1,10), '2019-01-0' + str(random.randint(1,9)), random.randint(1,1000), round(random.uniform(0,500),2)))
        conn.commit()
        cur.close()
        conn.close()
        print ('inserts complete')
    except psycopg2.Error as e:
        print (e)
        

def select():
    
    try:
        conn = psycopg2.connect("dbname=" + env_dbname + ' user=' + env_user +' password=' + env_pass + ' host=' + env_host)
        cur = conn.cursor()
        for dml in range(env_dmls):
            cur.execute("SELECT type.name, sum(transactions.quantity) FROM type INNER JOIN transactions on type.id = transactions.type GROUP BY type.name")
        cur.close()
        conn.close()
        #rows = cur.fetchall()
        #for row in rows:
        #    print (row)
        print ('selects complete')
    except psycopg2.Error as e:
        print (e)
        
    
def timer(button)

    return nothing