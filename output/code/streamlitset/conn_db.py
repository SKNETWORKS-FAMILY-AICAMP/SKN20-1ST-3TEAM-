import pymysql as mysql
import pymysql.cursors
# import mysql.connector as my
# from mysql.connector import Error
from dotenv import load_dotenv
import os
import pandas as pd

def get_connection():
    load_dotenv()

    return mysql.connect(
                host = os.getenv('DB_HOST'),
                user = os.getenv('DB_USER'),
                password = os.getenv('DB_PASSWORD'),
                port = int(os.getenv('DB_PORT')),
                database = 'sknfirst',
                cursorclass=mysql.cursors.DictCursor
    )

def load_home_data(sel_month) :
    try :
        with get_connection() as conn :
            print("Connected")
            with conn.cursor() as cur :
                sel_month = f'{sel_month}%'
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
                        WHERE c.report_month LIKE %s
                        GROUP BY sido;
                        '''
                cur.execute(query, (sel_month))
                results = cur.fetchall()

                df = pd.DataFrame(results)
                df.columns = ['시도명', '승용', '승합', '화물', '특수', '총계']

                # print(df)

                return df
    except Exception as e:
        print(e)

def load_home_data_by_sido(sel_month, sel_sido) :
    try :
        with get_connection() as conn :
            print("Connected")
            with conn.cursor() as cur :
                sel_month = f'{sel_month}%'
                query = '''
                        SELECT r.sigungu AS sigungu
                            , c.passenger_subtotal
                            , c.van_subtotal
                            , c.truck_subtotal
                            , c.special_subtotal
                            , c.total_subtotal
                        FROM car_registeration c
                        JOIN region r
                        ON c.region_id = r.region_id
                        WHERE c.report_month LIKE %s
                        AND r.sido LIKE %s;
                        '''
                cur.execute(query, (sel_month, sel_sido))
                results = cur.fetchall()

                df = pd.DataFrame(results)
                df.columns = ['시군구명', '승용', '승합', '화물', '특수', '총계']

                # print(df)

                return df
    except Exception as e:
        print(e)

def load_date_data() :
    try :
        with get_connection() as conn :
            print("Connected")
            with conn.cursor() as cur :
                query = '''
                        SELECT report_month 
                        FROM car_registeration
                        GROUP BY report_month
                        ORDER BY report_month DESC;
                        '''
                
                cur.execute(query)
                results = cur.fetchall()

                df = pd.DataFrame(results)

                # print(df)

                return df
    except Exception as e:
        print(e)

def load_detail_data(sel_month) :
    try :
        with get_connection() as conn :
            print("Connected")
            with conn.cursor() as cur :
                sel_month = f'{sel_month}%'
                query = '''
                        SELECT passenger_official
                            , passenger_private
                            , passenger_commercial
                            , van_official
                            , van_private
                            , van_commercial
                            , truck_official
                            , truck_private
                            , truck_commercial
                            , special_official
                            , special_private
                            , special_commercial
                        FROM car_registeration
                        WHERE report_month LIKE %s;
                        '''
                cur.execute(query, (sel_month))
                results = cur.fetchall()

                df = pd.DataFrame(results)

                print(df)

                return df
    except Exception as e:
        print(e)

def load_faq_data(view_state='전체', first_selection='전체', second_selection='전체', search_query='') :
    try :
        with get_connection() as conn :
            print("Connected")
            with conn.cursor() as cur :
                query_list = []
                condition_list = []
                default_query = '''
                        SELECT faq_company, faq_question, faq_answer 
                        FROM faq
                        '''
                query_list.append(default_query)

                if view_state != '전체' :
                    query_com = "WHERE faq_company = %s"
                    query_list.append(query_com)
                    condition_list.append(view_state)
                if first_selection != '전체' :
                    query_1 = "AND faq_major_category = %s"
                    query_list.append(query_1)
                    condition_list.append(first_selection)
                if second_selection != '전체' :
                    query_2 = "AND faq_sub_category = %s"
                    query_list.append(query_2)
                    condition_list.append(second_selection)
                if search_query != '':
                    search_query = f'%{search_query}%'
                    query_search = "AND faq_question LIKE %s"
                    query_list.append(query_search)
                    condition_list.append(search_query)

                query = " ".join(query_list)
                cur.execute(query, tuple(condition_list))

                results = cur.fetchall()

                df = pd.DataFrame(results)

                print(df)

                return df
    except Exception as e:
        print(e)