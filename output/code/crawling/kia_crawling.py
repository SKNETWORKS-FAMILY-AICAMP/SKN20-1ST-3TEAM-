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
import tqdm

# URL 설정
url = 'https://www.kia.com/kr/customer-service/center/faq/'
# 웹 드라이버 설치 및 최신버전 유지
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service = service)
driver.get(url)
# driver.maximize_window()
time.sleep(3)

# //*[@id="tab-list"]/li[2]/button
all_btn = driver.find_element(By.XPATH, '//*[@id="tab-list"]/li[2]/button')
driver.execute_script('arguments[0].click()', all_btn)
time.sleep(2)

faq_list = []
pag_num = 1

# soup = BeautifulSoup(driver.page_source, 'html.parser')
# str_table_rows = '#accordion-specification'
# table_rows = soup.select(str_table_rows)

# for i in table_rows :
#     str_q = i.span.text
#     print(i.span.text)
    
#     str_a = i.div.text.strip(str_q)
#     print(str_a)

for i in (range(1, 25)):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    str_table_rows = '.cmp-accordion__item'
    table_rows = soup.select(str_table_rows)

    for row in table_rows :
        temp_list = []
        
        str_q = row.span.text
        # print(str_q)
        temp_list.append(str_q)

        try :
            str_a = row.find('p').text
            # print(str_a)
            temp_list.append(str_a)
        except Exception as e:
            str_a = row.find('ul').text
            temp_list.append(str_a)

        faq_list.append(temp_list)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # page_list = soup.find(By.CLASS_NAME, 'paging-list')
    page_list = soup.select('.paging-list')
    pag_num += 1
    if i > 23 :
        break
    elif pag_num <= 5 :
        next_path = f'#contents > div > div.container.responsivegrid.aem-GridColumn.aem-GridColumn--default--12 > div > div > div.faq-bottom-paging.spacing-pt3.spacing-pb3 > div > ul > li:nth-child({pag_num}) > a'
    else :
        next_path = '#contents > div > div.container.responsivegrid.aem-GridColumn.aem-GridColumn--default--12 > div > div > div.faq-bottom-paging.spacing-pt3.spacing-pb3 > div > button.pagigation-btn-next'        
        pag_num = 1
    next_btn = driver.find_element(By.CSS_SELECTOR, next_path)
    driver.execute_script('arguments[0].click()', next_btn)

    # try :
    #     next_btn = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div/div[2]/div/div[1]/div[2]/nav/button[7]')
    #     driver.execute_script('arguments[0].click()', next_btn)
    # except :
    #     pass    # 마지막 페이지에서 Exception 발생
    
    time.sleep(2)

print(len(faq_list))
for i in faq_list :
    print(i)