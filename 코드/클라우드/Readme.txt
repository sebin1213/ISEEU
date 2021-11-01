@총 람다 갯수 8개 
    #
    team03-lambda-01 : s3 to rds (person) = lambda_function.py
    team03-lambda-02 : s3 to rds (person) = lambda_function2.py
    team03-lambda-03 : s3 to rds (person) = lambda_function3.py
    team03-lambda-04 : api - rds (person) = lambda_function4.py 
    team03-lambda-06 : api - rds (unknown_record) = lambda_function5.py
    team03-lambda-07 : api - rds (cctv_fire) = lambda_function6.py
    team03-lambda-08 : api -rds (cctvff_news) = lambda_function7.py
    team03-lambda-09 : api - rds (cctv_road) = lambda_function8.py

    # 람다에 사용된 라이브러리
    pymysql

@api gateway 1개
=>리소스 5개 , 메소드 5개 (GET), 스테이지 1개

    #1 fire 
    https://nwkzmmpf5l.execute-api.us-west-1.amazonaws.com/team03-database-api/big-fire-db-api

    #2 news
    https://nwkzmmpf5l.execute-api.us-west-1.amazonaws.com/team03-database-api/big-news-db-api

    #3 road
    https://nwkzmmpf5l.execute-api.us-west-1.amazonaws.com/team03-database-api/big-road-db-api

    #4 출입기록
    https://nwkzmmpf5l.execute-api.us-west-1.amazonaws.com/team03-database-api/iorecord-db-api

    #5 사용자(person)
    https://nwkzmmpf5l.execute-api.us-west-1.amazonaws.com/team03-database-api/person-db-api