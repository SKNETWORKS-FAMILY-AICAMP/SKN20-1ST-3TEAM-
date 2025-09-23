from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # enter키 등을 입력하기위해서
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import tqdm

# 시작년월과 끝년월 설정
START_YEAR = 2024
START_MONTH = 9

END_YEAR = 2024
END_MONTH = 11

# URL 설정
url = 'https://stat.molit.go.kr/portal/cate/statView.do?hRsId=58'

def set_city_list() :
    '''
    시군구 리스트를 불러오는 def
     - **return** city_list (**list**)
    '''
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # table의 시군구를 담아오기 위한 list 생성
    str_city_rows = '#sheet01-table > tbody > tr:nth-child(2) > td:nth-child(1) > div > div.GMPageOne > table > tbody > tr'
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
                    # print(j.text.strip())
                    city_list.append(j.text)
        except Exception as e:
            print(e)

    return city_list

def set_car_registeration(cur_year, cur_month) :
    '''
    각 년월에 자동차수등록현황를 불러오는 def
     - **input** cur_year (**int**), cur_month (**int**)
     - **return** month_lists (**list[list]**)
    '''
    # 기간 선택
    v_time = cur_year * 100 + cur_month

    select = Select(driver.find_element(By.ID, 'sStart'))
    select.select_by_value(str(v_time))
    time.sleep(0.5)
    select = Select(driver.find_element(By.ID, 'sEnd'))
    select.select_by_value(str(v_time))
    time.sleep(0.5)

    # 조회 버튼
    btn = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[3]/div/div[1]/div/div/div/button')
    driver.execute_script("arguments[0].click()", btn)
    time.sleep(1.5)

    # 시군구 리스트 가져오기
    city_list = set_city_list()
    
    # 데이터 가져오기
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    str_table_rows = '#sheet01-table > tbody > tr:nth-child(2) > td:nth-child(2) > div > div.GMPageOne > table > tbody > tr'
    month_rows = soup.select(str_table_rows)
    
    month_lists = []

    for idx, month_list in tqdm.tqdm(enumerate(month_rows), desc = f"{cur_year}-{cur_month} month list") :
        temp_list = []

        # 년월과 시군구 이름 추가
        temp_list.append(f'{v_time}01')
        temp_list.append(city_list[idx])
        
        # 데이터 추가 try
        try :
            city_month_list = month_list.select('td')
            for num in city_month_list :
                if not num.text == '' :
                    temp_list.append(int(num.text.replace(',', '')))
        except Exception as e:
            print(e)
        
        month_lists.append(temp_list)

    return month_lists

# 웹 드라이버 설치 및 최신버전 유지
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service = service)
driver.get(url)
# driver.maximize_window()
time.sleep(5)

# 시도별 자동차 등록 현황 조회
select = Select(driver.find_element(By.ID, 'sFormId'))
select.select_by_value('5498')
time.sleep(0.5)

form_btn = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[1]/div[2]/div/button')
driver.execute_script('arguments[0].click()', form_btn)
time.sleep(3)

# 선택을 위한 검색년월 (START부터)
# 전역 변수 설정은 14번째 줄
cur_year = START_YEAR
cur_month = START_MONTH

# 전체 데이터를 담을 list 생성
total_lists = []

while True :
    month_lists = set_car_registeration(cur_year, cur_month)
    
    # input data 확인
    # for i in month_lists[1:] :
    #   print(i)
    #   pass
    # print()

    # list에 데이터 추가
    # 이 부분 MySQL에 INSERT 하도록 변경
    total_lists.append(month_lists)
    
    cur_month += 1
    if cur_month > 12 :
        cur_year += 1
        cur_month = 1

    if cur_year * 100 + cur_month > END_YEAR * 100 + END_MONTH :
        break

time.sleep(2)
driver.quit()