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

# -----
# URL 설정
url = 'https://www.hyundai.com/kr/ko/faq.html'

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service = service)
driver.get(url)
driver.maximize_window()
time.sleep(3)

# INSERT query
sql = """
    INSERT INTO sknfirst.faq (
        faq_company, faq_major_category, faq_sub_category, faq_question, faq_answer
    ) VALUES (
        %s, %s, %s, %s, %s
    )
"""

faq_list = []

try:
    for i in tqdm.tqdm(range(1, 22)):
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        str_h_faq = '#contents > div.faq > div > div.section_white > div > div.result_area > div.ui_accordion.acc_01 > dl'
        h_faq = soup.select(str_h_faq)

        data_to_insert = []
        for item in h_faq:
            temp_list = []
            temp_list.append('현대')

            major_str, sub_str = item.i.text.split('>')
            major_str = major_str.replace('[', '').strip()
            sub_str = sub_str.replace(']', '').strip()
            temp_list.append(major_str)
            temp_list.append(sub_str)

            title_str = item.span.text.strip()
            temp_list.append(title_str)

            text_str = item.dd.text.strip()
            temp_list.append(text_str)

            data_to_insert.append(tuple(temp_list))
        
        # 데이터 삽입
        if data_to_insert:
            cursor.executemany(sql, data_to_insert)
            conn.commit()

        try:
            next_btn = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div/div[2]/div/div[1]/div[2]/nav/button[7]')
            driver.execute_script('arguments[0].click()', next_btn)
        except:
            pass
        time.sleep(3)
    
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