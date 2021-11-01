## Api to RDS lambda (Api to big RDS cctv_road table)


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
        sql = "select * from cctv_road "
        
        cursor.execute(sql)
        conn.commit()
        
        result = []
        

        for i in cursor:
            json_data = {}
            json_data['id'] = i[0]
            json_data['road_info'] = i[1]
            json_data['road_st_time'] = str(i[2])
            json_data['road_end_time'] = str(i[3])
            print(type(json_data['road_end_time']))
           
            result.append(json_data)
            
        return result
    except Exception as e:
        print("Database connection failed due to {}".format(e))