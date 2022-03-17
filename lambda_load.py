import json
import boto3 # library used to access AWS API
import os

def lambda_handler(event, context):
    os.chdir('/tmp')
    bucket = 'de-x3-lle-jupiter'
    filename = '/2022/3/16/chesterfield_16-03-2022_09-00-00.csv'
    client = boto3.client('s3')
    response = client.get_object(
    Bucket=bucket,
    Key=filename
    )
    
    print(response)
    