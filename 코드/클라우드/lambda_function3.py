## S3 to RDS lambda (S3 IO-Record to big data RDS unknown_record table)


import json
import urllib.parse
import boto3
import pymysql
import os





s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    region = event['Records'][0]['awsRegion']


    split1 = key.split('/',1) # split1 = ['Registered-User', 'user_100_20210528_085423.jpg']
    split2 = split1[1] # split2 = user_100_20210528_085423.jpg
    split3 = split2.split('_',4) # split3 = ['user', '100', '20210528', '085423.jpg']
    split4 = split3[2]+split3[3] # split4 = 20210522093355.jpg
    split5 = split4.split('.',1) # split5 = ['20210522093355', 'jpg']

    id = int(split3[1])
    name =split3[0]
    time = split5[0]
    split6 = split3[2]+'_'+split3[3] # split6 = 20210522_093355.jpg
    split7 = split6.split('.',1) # split7 = ['20210522_093355','jpg']
    video_time = split7[0]
    
    
    
    
    try:
       
        #DB연결1 빅데이
        db_config2 = json.loads(os.environ['db_config2'])
        conn2 = pymysql.connect(**db_config2)
        cursor2 = conn2.cursor()
        url1 = 'https://' + bucket + '.s3-' + region + '.amazonaws.com/' + key
        video_url = 'https://yangjae-team03-s3.s3-us-west-1.amazonaws.com/IO-Record-Video/'+video_time+'.avi'
        
        #전체가져옴
        sql = "select * from unknown_record "
        cursor2.execute(sql)
        
        print('현재id:', id) 
        print('현재이름 :', name)
        nickname = "default"
        for i in cursor2:
            
            
            if (i[1]==id) and (i[2]==name) :
                nickname = i[6]
            
                sql1 = "INSERT INTO unknown_record (id, name,time,url,video_url,nickname) values ('%d', '%s','%s','%s','%s','%s')"
                cursor2.execute(sql1 % (id, name,time,url1,video_url,nickname))
                conn2.commit()
                
                break
            
                
        sql1 = "INSERT INTO unknown_record (id, name,time,url,video_url,nickname) values ('%d', '%s','%s','%s','%s','%s')"
        cursor2.execute(sql1 % (id, name,time,url1,video_url,nickname))
        conn2.commit()
                
        
    

    except Exception as e:
        print("Database connection failed due to {}".format(e))