#!/usr/bin/python2.7
#
# Small script to show PostgreSQL and Pyscopg together
#

import psycopg2
import os
import random

env_inserts = int(os.environ.get("INSERTS"))
env_pass = os.environ.get("PASS")
env_user = os.environ.get("USER")
env_host = os.environ.get("HOST")
env_dbname = os.environ.get("DBNAME")

try:
    conn = psycopg2.connect("dbname=" + env_dbname + ' user=' + env_user +' password=' + env_pass + ' host=' + env_host)
    cur = conn.cursor()
    for dml in range(env_inserts):
        cur.execute("INSERT INTO transactions (type, date, quantity, price) VALUES (%s, %s, %s, %s)",(random.randint(1,10), '2019-01-0' + str(random.randint(1,9)), random.randint(1,1000), round(random.uniform(0,500),2)))
    conn.commit()
    conn.close()
    #rows = cur.fetchall()
    #for row in rows:
    #    print (row)
    print ('inserts complete')
except psycopg2.Error as e:
    print (e)
