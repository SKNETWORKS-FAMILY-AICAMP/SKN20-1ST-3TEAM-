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

start_year = 2024
start_month = 9

end_year = 2025
end_month = 3

cur_year = start_year
cur_month = start_month

total_lists = []

while True :
    # 기간 선택
    v_time = cur_year * 100 + cur_month

    select = Select(driver.find_element(By.ID, 'sStart'))
    select.select_by_value(str(v_time))
    time.sleep(0.5)
    select = Select(driver.find_element(By.ID, 'sEnd'))
    select.select_by_value(str(v_time))
    time.sleep(0.5)

    # 조회 버튼
    # //*[@id="main"]/div/div[2]/div[2]/div[3]/div/div[1]/div/div/div/button
    btn = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[3]/div/div[1]/div/div/div/button')
    driver.execute_script("arguments[0].click()", btn)
    time.sleep(1.5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    str_table_rows = '#sheet01-table > tbody > tr:nth-child(2) > td:nth-child(2) > div > div.GMPageOne > table > tbody > tr'
    month_rows = soup.select(str_table_rows)

    # print(month_rows, '\n')
    # print(month_rows.select('td')[1])

    month_lists = []

    for i in month_rows :
        temp_list = []

        try :
            i_list = i.select('td')
            for j in i_list :
                # print(j.text.strip())
                temp_list.append(j.text.strip())
        except Exception as e:
            print(e)
        
        month_lists.append(temp_list)

    print(v_time, month_lists[1])

    total_lists.append(month_lists)
    
    cur_month += 1
    if cur_month > 12 :
        cur_year += 1
        cur_month = 1

    if cur_year * 100 + cur_month > end_year * 100 + end_month :
        break

print(total_lists)

time.sleep(10)