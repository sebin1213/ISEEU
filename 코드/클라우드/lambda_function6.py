## Api to RDS lambda (Api to big RDS cctv_fire table)


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
        sql = "select * from cctv_fire "

        cursor.execute(sql)
        conn.commit()
        
  
        result = []
        

        for i in cursor:
            
            json_data = {}
            json_data['id'] = i[0]
            json_data['Fire_loc'] = i[1]# 유니코드
            json_data['Fire_time'] = str(i[2])
            json_data['Fire_state'] = i[3]
            json_data['Fire_area'] = i[4]
            result.append(json_data)
            print(json_data['Fire_time'])
            print(type(json_data['Fire_time']))
            

        return result
    except Exception as e:
        print("Database connection failed due to {}".format(e))