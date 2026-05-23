import time, pymysql, os

while True:
    try:
        pymysql.connect(
            host="mysql",
            user="root",
            password=os.getenv("MYSQL_ROOT_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )

        print("DB is ready!")
        break
    
    except Exception as e:
        print("Waiting DB...", e)
        time.sleep(7)