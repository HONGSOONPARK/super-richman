# -*- coding: utf-8 -*- 
#!/usr/bin/python3

import requests
import time
import pymysql
import json
import urllib.request
 
from datetime import datetime
from bs4 import BeautifulSoup

from urllib.parse import quote_plus    # 한글 텍스트를 퍼센트 인코딩으로 변환

from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait   # 해당 태그를 기다림
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException,StaleElementReferenceException    # 태그가 없는 예외 처리
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("disable-gpu") # 혹은 options.add_argument("--disable-gpu")
options.add_argument('lang=ko_KR')    # 언어 설정


# 드라이버는 운영체제&버전 맞는걸 다운받아서 사용하자
# https://chromedriver.chromium.org/downloads
driver = webdriver.Chrome('./chromedriver', options=options)   
driver.implicitly_wait(3)

wait = WebDriverWait(driver, 10)

# 버튼 Elements를 구함 
# clear  + 0.01 | + 0.1 | +1 | .....
def get_button_list():
    # div 의 개수를 구함
    buttonList = driver.find_elements(By.XPATH, '//*[@id="page-scroll"]/div[1]/div[2]/div/div[4]/div/div[2]/div/div')
    i = 0
    data = []
    print('\n## start buttonList')

    # 개수만큼 반복하며 하위 엘리먼트들을 구함, 굳이 이렇게 안해도되는데 걍 보라고함
    # 엘리먼트는 각자 개별로 구해도 되는데 이렇게 동적으로 구현 가능
    while i < len(buttonList) :      
        i += 1
        try:
            path =f'//*[@id="page-scroll"]/div[1]/div[2]/div/div[4]/div/div[2]/div/div[{i}]'
            element = driver.find_element(By.XPATH, path)
            data.append(element.get_attribute('innerText'))
        except Exception:
            print('오류 발생')    
    print(data)
            

# Previous Elements를 구함 
# last 100 .. 
def get_previous_count():
    previous =  driver.find_elements(By.XPATH, '//*[@id="page-scroll"]/div[1]/div[2]/div/div[3]/div/div[2]/div')
    i = 0
    data = []
    print('\n## start previous count')  
    while i < len(previous) :              
        i += 1
        try:
            path =f'//*[@id="page-scroll"]/div[1]/div[2]/div/div[3]/div/div[2]/div[{i}]'
            element = driver.find_element(By.XPATH, path)
            data.append(element.get_attribute('innerText'))
        except Exception:
            print('오류 발생')       
    print(data)


# Place Bet를 구함 
# Place Bet WIN 2X .. 
def get_place_bet():
    placeBet =  driver.find_elements(By.XPATH, '//*[@id="page-scroll"]/div[1]/div[2]/div/div[5]/div')
    i = 0
    data = []
    print('\n## start place bet')  
    while i < len(placeBet) :              
        i += 1
        try:
            path =f'//*[@id="page-scroll"]/div[1]/div[2]/div/div[5]/div[{i}]'
            element = driver.find_element(By.XPATH, path)
            data.append(element.get_attribute('innerText'))
        except Exception:
            print('오류 발생')       
    print(data)

try:    

    print('############ 크롤링 시작 ############ \n ')
    # driver connect
    driver.get('https://csgoempire.com/')
    headers = {'User-Agent':'Chrome/107.0.5304.121'}
   
    get_button_list()
    get_previous_count()
    get_place_bet()
   
except TimeoutException:
    print('타임아웃 발생 \n')

finally: 
    driver.quit()
    
print('############ 크롤링 끝 ############ \n ')




