# -*- coding: utf-8 -*- 

import requests
import time
import pymysql
import json

 
from datetime import datetime
from bs4 import BeautifulSoup

from urllib.parse import quote_plus    # 한글 텍스트를 퍼센트 인코딩으로 변환

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait   # 해당 태그를 기다림
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException,StaleElementReferenceException    # 태그가 없는 예외 처리
from selenium.webdriver.common.keys import Keys


options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu") # 혹은 options.add_argument("--disable-gpu")

options.add_argument('lang=ko_KR')    # 언어 설정
driver = webdriver.Chrome('/home/hs/Python/py/chromedriver', chrome_options=options)
driver.implicitly_wait(3)

wait = WebDriverWait(driver, 10)

# MySQL Connection 연결
conn = pymysql.connect(host='localhost', user='testhong', password='1234', db='testhong', charset='utf8') 



# css 체크 함수
def check_css(css_path, drv):
    try:
        drv.find_element_by_css_selector(css_path)
    except NoSuchElementException:
        return False
    return True


# xpath 체크 함수
def check_xpath(css_path, drv):
    try:
        drv.find_element_by_xpath(css_path)
    except NoSuchElementException:
        return False
    return True


# 파싱 데이터 json 으로 만듬
def parse_json(name, detail, url) :
    addr = ''
    tel = ''

    dtext = detail.text
    splt = dtext.split('\n')

    try:
        for li in splt :
            if '주소:' in li :
                addr = li.replace('주소: ','')
            if '연락처:' in li :
                tel = li.replace('연락처: ','')

        # mkat json
        makeJson = {
            'name' : name.text,
            'detail' : detail.text,
            'addr' : addr,
            'tel' : tel,
            'url' : url
        }
        # json type
        jsonString = json.dumps(makeJson)
    except Exception:
        print('json make 실패')
    
    finally : 
        print('json make 완료')    

    return jsonString


# xpath 체크 함수
def insert_data(data, tag):
    try:
        # Connection 으로부터 Cursor 생성
        curs = conn.cursor()

        jsonData = json.loads(data)
        # print(jsonData)
        name = jsonData['name']
        addr = jsonData['addr']
        tel = jsonData['tel'] 
        url = jsonData['url']
        detail = jsonData['detail']

        # SQL문 실행
        sql = 'INSERT INTO google_list (type, tag, name, addr, tel, url, detail) VALUES ("'+type_name+'","'+tag+'","'+name+'","'+addr+'","'+tel+'","'+url+'","'+detail+'")'
        curs.execute(sql)
    
        # 데이타 Fetch
        rows = curs.fetchall()

    except Exception:
        print('인서트 실패')

    finally:
        print('작업종료')



try:    # 정상 처리

    type_name = 'emoney'
    tag = type_name+'_'+datetime.today().strftime("%Y%m%d%H%M%S")

    driver.get('https://www.google.com/')
    f = open("/home/hs/Python/py/log_"+tag+".txt", 'w', encoding="UTF8")
    f.write(tag+'\n')

    time.sleep(2) # 웹페이지를 불러오기 위해 2초 정지

    # 검색창 # 해당 태그 존재 여부를 확인하기까지 3초 정지
    search_input_tag = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input')))
  
    # 검색창에 키워드 입력
    keyword = "공덕역 밥집"
    search_input_tag.send_keys(keyword)

    # 엔터키 입력
    search_input_tag.send_keys(Keys.ENTER)
    time.sleep(1)

    # 장소 더 보기 버튼
    path = '//*[@id="rso"]/div[1]/div/div[2]/div/div[4]/div[3]/div/div/a/div/span'
    more = wait.until(EC.element_to_be_clickable((By.XPATH, path)))
    more.click()

    time.sleep(2)

    
    # 페이지 개수 구하기
    path = '//*[@id="rl_ist0"]/div[2]/div/table/tbody/tr/td'
    page_count = driver.find_elements_by_xpath(path)
    print(len(page_count))


    # 리스트 클릭했을때 나오는 부분 id가 자꾸 바뀌어서 체크하기 위해서 만듬 ..
    checkWrap = True
    g_path = ''
    v = 1
    l = 0
    while(checkWrap) :
        path =f'//*[@id="akp_tsuid{v}"]'

        if(v > 100) :
            raise Exception('상세 못찾음..') 
        if check_xpath(path, driver):
            checkWrap = False
            g_path = path
        else :
            v = v + 1     
    # ================================================================
    # 페이지 9번 돈다
    while l < 9 :
        print('순서', l)
        l += 1
        # 들어왔는지 체크 ('평점' Element 확인)
        path = '//*[@id="rllhd__fldhc"]/div/div/div/div/div[1]/div/div[1]/div/span[1]'
        element = wait.until(EC.presence_of_element_located((By.XPATH, path)))
        print(element.text) 
        print('============================================')

        # 전체 리스트 갯수 구하기
        path = '//*[@id="rl_ist0"]/div[1]/div[4]/div'
        list_count = driver.find_elements_by_xpath(path)

        print('전체 리스트:',len(list_count))

        
        # 식당 리스트 만큼 반복
        i = 0
        while i < len(list_count) :            
            i += 1
            path =f'//*[@id="rl_ist0"]/div[1]/div[4]/div[{i}]'

            wrap = driver.find_element_by_xpath(path)

            path = path + '/div/div[2]/div/a/div/div[2]/div'
            
            wait_txt = WebDriverWait(wrap, 1)
            path = 'div > div.uMdZh.rl-qs-crs-t.mnr-c > div > a > div > div.dbg0pd > div'

            # 식당이름 리스트 클릭
            if check_css(path, wrap) :
                list_wrap = wait_txt.until(EC.presence_of_element_located((By.CSS_SELECTOR, path)))
                list_wrap.click()
            else : 
                print('클릭 실패')
                continue
            
            time.sleep(1)
   
            if check_xpath(g_path, driver) :
                detail_wrap = driver.find_element_by_xpath(g_path)
                # 상세보기
                # if -> 다른 element 사용하는 경우가 있음
                try:

                    # 식당 이름
                    path = g_path + '/div/div[1]/div/div/div/div[1]/div/div[1]/div/div[1]/div/div[1]/div/div[1]/div/span'
                    if check_xpath(path, detail_wrap) is False :
                        path = g_path + '/div/div[1]/div/div/div/div[1]/div/div[1]/div/div[1]/div/div[1]/div/div[2]/div[1]/span'
                        
                    name = detail_wrap.find_element_by_xpath(path)
                    # print(name.text) 

                    # 이하 상세정보
                    path = g_path + '/div/div[1]/div/div/div/div[1]/div/div[1]/div/div[3]/div'
                    if check_xpath(path, detail_wrap) is False :
                        path = g_path + '/div/div[1]/div/div/div/div[1]/div/div[1]/div/div[3]/div'
                    detail = detail_wrap.find_element_by_xpath(path)
                    # print(detail.text) 

                    curl = driver.current_url
                    # print(curl) 

                    f.write(name.text +'\n')
                    f.write(detail.text +'\n')
                    f.write(curl + '\n')
                    f.write('===============\n')
                    
                    # 파싱한 데이터 가공
                    jsonData = parse_json(name, detail, curl)
            
                    # mysql insert
                    insert_data(jsonData, tag)

                except Exception:
                    print('찾기실패')
                finally :
                    time.sleep(3)

            else :
                print('상세 정포 파싱 실패, log, db insert 안됨')
                # raise Exception('상세 못찾음') 
                continue
            print('============================================')

        print('다음 페이지 클릭')
       
        # 제일 아래까지 내릴 경우
        try:
            path = '//*[@id="rl_ist0"]'
            list_wrap = driver.find_element_by_xpath(path)
            target = list_wrap.find_element_by_link_text('다음')
            target.location_once_scrolled_into_view
            target.click()
        except Exception:
            print('다음 페이지 클릭 실패')    
        finally :
            time.sleep(5)

except TimeoutException:    # 예외 처리
    print('타임아웃 발생')

finally:    # 정상, 예외 둘 중 하나여도 반드시 실행
    driver.quit()
    f.close()



print('크롤링 끝')

