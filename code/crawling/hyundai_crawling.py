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
url = 'https://www.hyundai.com/kr/ko/faq.html'
# 웹 드라이버 설치 및 최신버전 유지
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service = service)
driver.get(url)
# driver.maximize_window()
time.sleep(3)

faq_list = []

for i in tqdm.tqdm(range(1, 22)):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    str_h_faq = '#contents > div.faq > div > div.section_white > div > div.result_area > div.ui_accordion.acc_01 > dl'
    h_faq = soup.select(str_h_faq)

    for idx, i in enumerate(h_faq) :
        temp_list = []
        temp_list.append('현대')

        major_str, sub_str = i.i.text.split('>')
        major_str = major_str.replace('[', '').strip()
        sub_str = sub_str.replace(']', '').strip()
        # print(major_str, sub_str)
        temp_list.append(major_str)
        temp_list.append(sub_str)

        title_str = i.span.text.strip()
        # print(title_str)
        temp_list.append(title_str)

        text_str = i.dd.text.strip()
        # print(text_str)
        temp_list.append(text_str)

        faq_list.append(temp_list)

    # for i in faq_list :
    #     print(i)

    try :
        next_btn = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div/div[2]/div/div[1]/div[2]/nav/button[7]')
        driver.execute_script('arguments[0].click()', next_btn)
    except :
        pass    # 마지막 페이지에서 Exception 발생
    time.sleep(3)

print(len(faq_list))
# for i in faq_list :
#     print(i[:-1])