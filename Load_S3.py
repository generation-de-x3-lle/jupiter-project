import json
import boto3 # library used to access AWS API
import os
import codecs
import csv
import datetime

def lambda_handler(event, context):
    listofdicts=[] 
    fieldnames =['Date','Location','name','product','total','payment_method','card_number']
    os.chdir('/tmp')
    bucket = 'de-x3-lle-jupiter'
    filename = '2022/3/16/chesterfield_16-03-2022_09-00-00.csv'
    client = boto3.client('s3')
    response = client.get_object(
    Bucket=bucket,
    Key=filename
    )
    
    for rows in csv.DictReader(codecs.getreader("utf-8")(response["Body"]),fieldnames=fieldnames):

        listofdicts.append(rows)

    return listofdicts