from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
db_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME"),
    'port': os.getenv("DB_PORT") }

sql = """
    INSERT INTO car_registeration 
    (report_month, region_id,
     passenger_official, passenger_private, passenger_commercial, passenger_subtotal,
     van_official, van_private, van_commercial, van_subtotal,
     truck_official, truck_private, truck_commercial, truck_subtotal,
     special_official, special_private, special_commercial, special_subtotal,
     total_official, total_private, total_commercial, total_subtotal)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
    passenger_official=VALUES(passenger_official), passenger_private=VALUES(passenger_private),
    passenger_commercial=VALUES(passenger_commercial), passenger_subtotal=VALUES(passenger_subtotal),
    van_official=VALUES(van_official), van_private=VALUES(van_private),
    van_commercial=VALUES(van_commercial), van_subtotal=VALUES(van_subtotal),
    truck_official=VALUES(truck_official), truck_private=VALUES(truck_private),
    truck_commercial=VALUES(truck_commercial), truck_subtotal=VALUES(truck_subtotal),
    special_official=VALUES(special_official), special_private=VALUES(special_private),
    special_commercial=VALUES(special_commercial), special_subtotal=VALUES(special_subtotal),
    total_official=VALUES(total_official), total_private=VALUES(total_private),
    total_commercial=VALUES(total_commercial), total_subtotal=VALUES(total_subtotal)
"""

# ----
# 시작년월과 끝년월 설정
START_YEAR = 2023
START_MONTH = 8
END_YEAR = 2025
END_MONTH = 8

def set_city_list(driver): # driver를 인자로 받도록 수정
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    str_city_rows = '#sheet01-table > tbody > tr:nth-child(2) > td:nth-child(1) > div > div.GMPageOne > table > tbody'
    city_rows = soup.select(str_city_rows)
    city_list = []
    for i in city_rows :
        rlg = ''
        try :
            i_list = i.select('td')
            for j in i_list :
                if j.text in ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '충북', '충남', '전남', '경북', '경남', '제주', '강원', '전북'] :
                    rlg = j.text.strip()
                elif not j.text in ['', '2025-08']:
                    city_list.append(j.text.strip()) # strip() 추가
        except Exception as e:
            print(e)
    return city_list

# URL 설정
url = 'https://stat.molit.go.kr/portal/cate/statView.do?hRsId=58'
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service = service)


try:
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    cursor.execute("SELECT region_id, sigungu FROM region")
    all_region_records = cursor.fetchall()
    region_map = {sigungu: region_id for region_id, sigungu in all_region_records}
    
    print(f"DB에서 {len(region_map)}개의 모든 지역 ID를 로드했습니다.")
    
    # 시도별 자동차 등록 현황 조회
    select = Select(driver.find_element(By.ID, 'sFormId'))
    select.select_by_value('5498')
    time.sleep(0.5)

    form_btn = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[1]/div[2]/div/button')
    driver.execute_script('arguments[0].click()', form_btn)
    time.sleep(3)

    cur_year = START_YEAR
    cur_month = START_MONTH

    while True :
        v_time = cur_year * 100 + cur_month

        select = Select(driver.find_element(By.ID, 'sStart'))
        select.select_by_value(str(v_time))
        time.sleep(0.5)
        select = Select(driver.find_element(By.ID, 'sEnd'))
        select.select_by_value(str(v_time))
        time.sleep(0.5)

        btn = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[3]/div/div[1]/div/div/div/button')
        driver.execute_script("arguments[0].click()", btn)
        time.sleep(1.5)

        city_list = set_city_list(driver)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        str_table_rows = '#sheet01-table > tbody > tr:nth-child(2) > td:nth-child(2) > div > div.GMPageOne > table > tbody > tr'
        month_rows = soup.select(str_table_rows)
        
        month_lists = []
        city_name = set()
        for idx, month_list in enumerate(month_rows):
            temp_list = []
            try:
                temp_list.append(f'{v_time}01')
                city_name.add(city_list[idx])
                temp_list.append(city_list[idx])
                
                i_list = month_list.select('td')
                for j in i_list:
                    if not j.text == '':
                        temp_list.append(int(j.text.replace(',', '')))
            except Exception as e:
                print(e)
        
            if len(temp_list) > 2:
                month_lists.append(temp_list)


        for row_data in month_lists:
            try:
                # [날짜, 시군구, 숫자...] 형식의 데이터 분리
                date_str = row_data[0]
                sigungu_name = row_data[1]
                numeric_data = row_data[2:]

                # YYYYMMDD -> YYYY-MM-DD 형식으로 변환
                report_month = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"

                # region_map에서 지역 ID 조회
                region_id = region_map.get(sigungu_name)
                
                if region_id is None:
                    continue # region 테이블에 없는 지역이면 건너뛰기

                data_to_insert = (report_month, region_id) + tuple(numeric_data)

                if len(data_to_insert) == 22: #
                    cursor.execute(sql, data_to_insert)
                
            except Exception as e:
                print(e)
        
        
        conn.commit()
        print(f"{cur_year}년 {cur_month}월 데이터 저장됨")
        
        cur_month += 1
        if cur_month > 12 :
            cur_year += 1
            cur_month = 1

        if cur_year * 100 + cur_month > END_YEAR * 100 + END_MONTH :
            break

    time.sleep(2)

finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
    driver.quit()


