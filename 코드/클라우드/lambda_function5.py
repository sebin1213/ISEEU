## Api to RDS lambda (Api to big RDS unknown_record table)

import json
import urllib.parse
import pymysql
import os

#DB연결
db_config = json.loads(os.environ['db_config'])
conn = pymysql.connect(**db_config)
cursor = conn.cursor()


def lambda_handler(event, context):
    
    try:
        sql = "select * from unknown_record order by time DESC "
    
        cursor.execute(sql)
        conn.commit()
        
        result = []

        
        
        
        for i in cursor:
            json_data = {}
            json_data['id'] = i[1]
            json_data['name'] = i[2]
            
            json_data['time'] = str(i[3])
            json_data['url'] = i[4]
            json_data['video_url'] = i[5]
            json_data['nickname'] = i[6]
            result.append(json_data)
            print(json_data['time'])
            print(type(json_data['time']))
            

        return result
    except Exception as e:
        print("Database connection failed due to {}".format(e))