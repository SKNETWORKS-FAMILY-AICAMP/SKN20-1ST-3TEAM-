from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
import mysql.connector
from dotenv import load_dotenv
import os


def get_regions_from_website():
    url = 'https://stat.molit.go.kr/portal/cate/statView.do?hRsId=58'
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    city_list = []
    
    try:
        driver.get(url)
        driver.maximize_window()
        time.sleep(5)

        # 시도별 자동차 등록 현황 조회 
        select = Select(driver.find_element(By.ID, 'sFormId'))
        select.select_by_value('5498') 
        time.sleep(0.5)

        form_btn = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[1]/div[2]/div/button')
        driver.execute_script('arguments[0].click()', form_btn)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # 참고: 이 선택자는 매우 구체적이어서 웹사이트 구조 변경 시 깨질 수 있습니다.
        str_table_rows = '#sheet01-table > tbody > tr:nth-child(2) > td:nth-child(1) > div > div.GMPageOne > table > tbody'
        city_rows = soup.select(str_table_rows)

        # 광역자치단체와 구를 튜플 형태로 묶어서 list에 추가
        for i in city_rows:
            rlg = ''
            try:
                i_list = i.select('td')
                for j in i_list:
                    if j.text.strip() in ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '충북', '충남', '전남', '경북', '경남', '제주', '강원', '전북']:
                        rlg = j.text.strip()
                    elif j.text.strip() and not '2025' in j.text.strip():
                        city_list.append((rlg, j.text.strip()))
            
            except Exception as e:
                print(e)

        print(city_list)
        return city_list

    finally:
        driver.quit()


# -----
def save_regions_to_db(region_list):
    if not region_list:
        print("데이터 없음")
        return

    load_dotenv()
    db_config = {
        'host': os.getenv("DB_HOST"), 'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"), 'database': os.getenv("DB_NAME"),
        'port': os.getenv("DB_PORT")
    }

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql = "INSERT IGNORE INTO region (sido, sigungu) VALUES (%s, %s)"
        
        cursor.executemany(sql, region_list)
        conn.commit()
        
        print(f"{cursor.rowcount}개의 지역 추가 완료")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == '__main__':
    scraped_regions = get_regions_from_website()
    save_regions_to_db(scraped_regions)
