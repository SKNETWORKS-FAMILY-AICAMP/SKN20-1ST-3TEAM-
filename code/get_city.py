from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # enter키 등을 입력하기위해서
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time

# URL 설정
url = 'https://stat.molit.go.kr/portal/cate/statView.do?hRsId=58'
# 웹 드라이버 설치 및 최신버전 유지
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service = service)
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

# 시군구 이름을 가져오기 위한 parser
soup = BeautifulSoup(driver.page_source, 'html.parser')
str_table_rows = '#sheet01-table > tbody > tr:nth-child(2) > td:nth-child(1) > div > div.GMPageOne > table > tbody'
city_rows = soup.select(str_table_rows)

city_list = []

# 광역자치단체와 구를 튜플 형태로 묶어서 list에 추가
for i in city_rows :
    rlg = ''
    try :
        i_list = i.select('td')
        for j in i_list :
            if j.text in ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '충북', '충남', '전남', '경북', '경남', '제주', '강원', '전북'] :
                rlg = j.text.strip()
            elif not j.text in ['', '2025-08']:
                print(j.text.strip())
                city_list.append((rlg, j.text))
            
    except Exception as e:
        print(e)

print(len(city_list), city_list)