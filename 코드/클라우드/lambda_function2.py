## S3 to RDS lambda (S3 UnRegistered-User to RDS Person table)

import json
import urllib.parse
import boto3
import pymysql
import os

#DB연결
db_config = json.loads(os.environ['db_config'])
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    region = event['Records'][0]['awsRegion']
    
    
    split1 = key.split('/',1) # split1 = ['Registered-User', '1_unknown.jpg']
    split2 = split1[1] # split2 = 1_unknown.jpg
    split3 = split2.split('_',1) # split3 = ['1', 'unknown.jpg']
    split4 = split3[1] # split4 = 'unknown.jpg'
    split5 = split4.split('.',1) #split5 = ['unknown' , 'jpg']
    name = split5[0]
    id = int(split3[0])



    nickname = "default"
    
    try:
        url = 'https://' + bucket + '.s3-' + region + '.amazonaws.com/' + key
        sql = "INSERT INTO person (id, name,url,nickname) values ('%d','%s','%s','%s')"
        cursor.execute(sql % (id, name,url,nickname))
        conn.commit()
        return {
        'statusCode': 200
        }
    except Exception as e:
        print("Database connection failed due to {}".format(e))