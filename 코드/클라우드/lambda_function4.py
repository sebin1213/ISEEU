## Api to RDS lambda (Api to RDS person table)


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
        sql = "select * from person "
   
        cursor.execute(sql)
        conn.commit()
     
        result = []
        
 
        
  
        for i in cursor:
            json_data = {}
            json_data['id'] = i[1]
            json_data['name'] = i[2]
            
            json_data['url'] = i[3]
            json_data['nickname'] = i[4]
            result.append(json_data)
    
            

        return result
    except Exception as e:
        print("Database connection failed due to {}".format(e))