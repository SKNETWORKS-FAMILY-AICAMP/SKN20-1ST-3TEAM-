from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time
import tqdm
import pymysql
import os
from dotenv import load_dotenv


load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT', 3306) 

conn = None
cursor = None
try:
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        port=int(DB_PORT),
        charset='utf8'
    )
    cursor = conn.cursor()
    print("연결")
except pymysql.MySQLError as e:
    print(e)
    exit()


url = 'https://www.kia.com/kr/customer-service/center/faq/'

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(url)
driver.maximize_window()
time.sleep(3)

all_btn = driver.find_element(By.XPATH, '//*[@id="tab-list"]/li[2]/button')
driver.execute_script('arguments[0].click()', all_btn)
time.sleep(2)


sql = """
    INSERT INTO sknfirst.faq (
        faq_company, faq_major_category, faq_sub_category, faq_question, faq_answer
    ) VALUES (
        %s, %s, %s, %s, %s
    )
"""


faq_list = []
pag_num = 1
company = '기아'

try:
    for i in tqdm.tqdm(range(1, 25)):
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        str_table_rows = '.cmp-accordion__item'
        table_rows = soup.select(str_table_rows)

        data_to_insert = []
        for row in table_rows:
            str_q = row.span.text
            
            # 답변(answer) 추출
            try:
                # <p> 태그의 텍스트
                str_a = row.find('p').text.strip()
            except AttributeError:
                # <p> 태그가 없으면 <ul> 태그의 텍스트
                try:
                    str_a = row.find('ul').text.strip()
                except AttributeError:
                    str_a = '답변 없음' # 답변이 없는 경우

            # FAQ 카테고리가 없으므로 '기타'로 임시 처리
            temp_list = (company, '기타', '기타', str_q, str_a)
            data_to_insert.append(temp_list)

        # MySQL에 데이터 삽입
        if data_to_insert:
            cursor.executemany(sql, data_to_insert)
            conn.commit()

        
        pag_num += 1
        if i >= 24: # 루프가 24번 돌면 종료
            break
        
        # 다음 페이지 버튼 찾기
        next_btn = None
        if pag_num <= 5:
            # 1~5페이지 버튼
            next_path = f'#contents > div > div.container.responsivegrid.aem-GridColumn.aem-GridColumn--default--12 > div > div > div.faq-bottom-paging.spacing-pt3.spacing-pb3 > div > ul > li:nth-child({pag_num}) > a'
            next_btn = driver.find_element(By.CSS_SELECTOR, next_path)
        else:
            # '다음' 버튼
            next_path = '#contents > div > div.container.responsivegrid.aem-GridColumn.aem-GridColumn--default--12 > div > div > div.faq-bottom-paging.spacing-pt3.spacing-pb3 > div > button.pagigation-btn-next'
            next_btn = driver.find_element(By.CSS_SELECTOR, next_path)
            # '다음' 버튼 클릭 후 페이지 번호 초기화
            pag_num = 1

        driver.execute_script('arguments[0].click()', next_btn)
        time.sleep(2)
        
    print("DB삽입 완료")

except Exception as e:
    print(e)
    if conn:
        conn.rollback() 

finally:
    
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    driver.quit() 