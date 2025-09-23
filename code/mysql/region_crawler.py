from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select

# DB 저장을 위한 라이브러리
import mysql.connector
from dotenv import load_dotenv
import os


def get_regions_from_website():
    print("--- 지역 목록 크롤링을 시작합니다 ---")
    url = 'https://stat.molit.go.kr/portal/cate/statView.do?hRsId=58'
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    city_list = []
    
    try:
        driver.get(url)
        driver.maximize_window()
        time.sleep(5)

        # 시도별 자동차 등록 현황 조회 (현재 '서울'만 선택된 상태)
        select = Select(driver.find_element(By.ID, 'sFormId'))
        select.select_by_value('5498') # '서울'
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
                    # '서울'이라는 텍스트를 만나면 rlg 변수에 저장
                    if j.text.strip() in ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '충북', '충남', '전남', '경북', '경남', '제주', '강원', '전북']:
                        rlg = j.text.strip()
                    # 빈 값이 아니면 (rlg, 시군구) 형태로 추가
                    elif j.text.strip() and not '2025' in j.text.strip():
                        city_list.append((rlg, j.text.strip()))
            
            except Exception as e:
                print(f"파싱 중 오류: {e}")
        
        print(f"크롤링 완료: 총 {len(city_list)}개의 지역을 찾았습니다.")
        print(city_list)
        return city_list

    finally:
        driver.quit()

# ===================================================================
# 2. DB에 저장하는 함수
# ===================================================================
def save_regions_to_db(region_list):
    if not region_list:
        print("저장할 지역 데이터가 없습니다.")
        return

    print("\n--- DB에 지역 정보 저장을 시작합니다 ---")
    load_dotenv()
    db_config = {
        'host': os.getenv("DB_HOST"), 'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"), 'database': os.getenv("DB_NAME"),
        'port': os.getenv("DB_PORT")
    }

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        print(f"✅ MySQL '{db_config['database']}' DB에 성공적으로 연결되었습니다!")

        sql = "INSERT IGNORE INTO region (sido, sigungu) VALUES (%s, %s)"
        
        cursor.executemany(sql, region_list)
        conn.commit()
        
        print(f"DB 저장 완료: {cursor.rowcount}개의 새로운 지역이 추가되었습니다.")

    except mysql.connector.Error as err:
        print(f"MySQL 오류: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("🔌 MySQL 연결이 종료되었습니다.")

# ===================================================================
# 3. 메인 실행 부분
# ===================================================================
if __name__ == '__main__':
    # 1. 보내주신 코드로 크롤링 실행
    scraped_regions = get_regions_from_website()
    
    # 2. 크롤링 결과가 있으면 DB에 저장
    save_regions_to_db(scraped_regions)
