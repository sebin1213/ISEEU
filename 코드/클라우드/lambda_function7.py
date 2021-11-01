## Api to RDS lambda (Api to big RDS cctv_news table)


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
        sql = "select * from cctv_news "
        
        cursor.execute(sql)
        conn.commit()
        print(cursor)
        #a = cursor.execute(sql)
        result = []
        
        
        # for b in cursor:
        #      print(b)
        #      print(type(b))
        
        for i in cursor:
            json_data = {}
            json_data['id'] = i[0]
            json_data['News_title'] = i[1]
            json_data['News_href'] = i[3]
            json_data['News_writer'] = i[4]
            json_data['News_write_time'] = str(i[5])
            json_data['News_area'] = i[6]
            result.append(json_data)
            
        print(result)
        return result
    except Exception as e:
        print("Database connection failed due to {}".format(e))