from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time
import mysql.connector
from dotenv import load_dotenv
import os

# ===================================================================
# DB 저장 함수
# ===================================================================
def save_to_db(all_monthly_data, sido_name):
    print(f"\n--- [{sido_name}] car_registeration 테이블 저장을 시작합니다 ---")
    load_dotenv()
    db_config = {
        'host': os.getenv("DB_HOST"), 'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"), 'database': os.getenv("DB_NAME"),
        'port': os.getenv("DB_PORT")
    }

    conn = None
    cursor = None
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        print(f"✅ [{sido_name}] MySQL DB에 성공적으로 연결되었습니다!")

        # '서울'에 해당하는 모든 시군구의 ID를 미리 가져와 딕셔너리로 만듭니다.
        cursor.execute("SELECT id, sigungu FROM region WHERE sido = %s", (sido_name,))
        region_records = cursor.fetchall()
        region_map = {sigungu: id for id, sigungu in region_records}
        print(f"✔️ '{sido_name}'의 지역 ID {len(region_map)}개를 DB에서 로드했습니다.")

        sql = """
            INSERT INTO car_registeration 
            (report_month, region_id,
             total_subtotal, total_compact, total_small, total_midsize, total_large,
             official_subtotal, official_compact, official_small, official_midsize, official_large,
             private_subtotal, private_compact, private_small, private_midsize, private_large)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            total_subtotal=VALUES(total_subtotal), total_compact=VALUES(total_compact),
            total_small=VALUES(total_small)
        """
        
        for month_data in all_monthly_data:
            date_code = month_data['date_code']
            table_data = month_data['table_data']
            
            year, month = str(date_code)[:4], str(date_code)[4:]
            report_month = f"{year}-{month}-01"
            print(f"--- [{sido_name}] {report_month} 데이터 저장 중 ---")
            
            for row in table_data:
                try:
                    if not row or len(row) < 18 or row[0] in ['시군구', '소계']:
                        continue
                    
                    sigungu_name = row[0]
                    region_id = region_map.get(sigungu_name)

                    if region_id is None:
                        print(f"⚠️ region 테이블에 '{sigungu_name}'이 없습니다. 건너뜁니다.")
                        continue
                    
                    numeric_data = [int(item.replace(',', '')) for item in row[1:18]]
                    data_to_insert = (report_month, region_id) + tuple(numeric_data)
                    cursor.execute(sql, data_to_insert)

                except ValueError:
                    print(f"⚠️ 숫자 변환 불가로 다음 행을 건너뜁니다: {row[0]}")
                    continue
        
        conn.commit()
        print(f"\n🎉 [{sido_name}] 모든 데이터를 DB에 성공적으로 저장했습니다!")

    except mysql.connector.Error as err:
        print(f"❌ [{sido_name}] MySQL 오류: {err}")
        if conn: conn.rollback()
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected():
            conn.close()
            print(f"🔌 [{sido_name}] MySQL 연결이 종료되었습니다.")

# ===================================================================
# 웹 크롤링 함수 (보내주신 코드 기반)
# ===================================================================
def main_crawling(sido_name, sido_value):
    print(f"--- [{sido_name}] 크롤링을 시작합니다 ---")
    url = 'https://stat.molit.go.kr/portal/cate/statView.do?hRsId=58'
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        driver.get(url)
        driver.maximize_window()
        time.sleep(5)

        select = Select(driver.find_element(By.ID, 'sFormId'))
        select.select_by_value(sido_value)
        time.sleep(0.5)

        form_btn = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[1]/div[2]/div/button')
        driver.execute_script('arguments[0].click()', form_btn)
        time.sleep(3)

        start_year, start_month = 2024, 1
        end_year, end_month = 2024, 6
        cur_year, cur_month = start_year, start_month
        total_lists = []
        wait = WebDriverWait(driver, 10) # WebDriverWait 객체를 미리 생성

        while True:
            v_time = cur_year * 100 + cur_month
            print(f"... [{sido_name}] {cur_year}년 {cur_month}월 데이터 크롤링 중 ...")
            
            try:
                select = Select(driver.find_element(By.ID, 'sStart'))
                select.select_by_value(str(v_time))
                time.sleep(0.5)
                select = Select(driver.find_element(By.ID, 'sEnd'))
                select.select_by_value(str(v_time))
                time.sleep(0.5)

                search_button_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[3]/div/div/div/button'
                btn = wait.until(
                    EC.element_to_be_clickable((By.XPATH, search_button_xpath))
                )
                driver.execute_script("arguments[0].click()", btn)
                
                # ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
                # [수정] 조회 버튼 클릭 후, 실제 데이터 테이블이 나타날 때까지 기다립니다.
                # ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
                table_rows_selector = '#sheet01-table > tbody > tr:nth-child(2) > td:nth-child(2) > div > div.GMPageOne > table > tbody > tr'
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, table_rows_selector)))
                # ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

            except Exception as e:
                print(f"페이지 조작 중 오류 발생: {e}")
                break

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # 위에서 기다린 selector와 동일한 것을 사용합니다.
            month_rows = soup.select(table_rows_selector)

            month_lists = []
            for i in month_rows:
                temp_list = [j.text.strip() for j in i.find_all(['th', 'td'])]
                if temp_list:
                    month_lists.append(temp_list)

            total_lists.append({'date_code': v_time, 'table_data': month_lists})
            
            cur_month += 1
            if cur_month > 12:
                cur_year += 1
                cur_month = 1
            
            if cur_year * 100 + cur_month > end_year * 100 + end_month:
                break
        
        print(f"\n--- [{sido_name}] 크롤링 완료 ---")
        return total_lists

    finally:
        driver.quit()

# ===================================================================
# 메인 실행 부분
# ===================================================================
if __name__ == '__main__':
    # 보내주신 코드가 서울만 조회하므로, 서울 정보만 사용합니다.
    sido_info = {'name': '서울', 'value': '5498'}
    
    # 1. 크롤링 실행
    crawled_data = main_crawling(sido_name=sido_info['name'], sido_value=sido_info['value'])
    
    # 2. 크롤링된 데이터가 있으면 DB에 저장
    if crawled_data:
        save_to_db(crawled_data, sido_name=sido_info['name'])
    else:
        print("크롤링된 데이터가 없습니다.")