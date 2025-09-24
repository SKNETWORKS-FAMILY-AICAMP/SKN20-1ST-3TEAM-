import pymysql as mysql
import pymysql.cursors
# import mysql.connector as my
# from mysql.connector import Error
from dotenv import load_dotenv
import os
import pandas as pd

# load_dotenv()

def get_connection():
    return mysql.connect(
                host = '127.0.0.1',
                user = 'root',
                password = 'root1234',
                port = 3306,
                database = 'sknfirst',
                cursorclass=mysql.cursors.DictCursor
    )

def load_home_data() :
    with get_connection() as conn :
        print("Connected")
        with conn.cursor() as cur :
            query = '''
                    SELECT r.sido AS sido
                        , SUM(c.passenger_subtotal) AS passenger_total
                        , SUM(c.van_subtotal) AS van_total
                        , SUM(c.truck_subtotal) AS truck_total
                        , SUM(c.special_subtotal) AS special_total
                        , SUM(c.total_subtotal) AS total
                    FROM car_registeration c
                    JOIN region r
                    ON c.region_id = r.region_id
                    WHERE c.report_month LIKE '2025-08%'
                    GROUP BY sido;
                    '''
            cur.execute(query)
            results = cur.fetchall()

            df = pd.DataFrame(results)
            df.columns = ['시도명', '승용', '승합', '화물', '특수', '총계']

            print(df)

            return df