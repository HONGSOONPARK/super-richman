from pykrx import stock
import requests
import json
from pandas import json_normalize

import time
import pymysql
import pandas as pd
from sqlalchemy import create_engine

# dataframe inert mysql
pymysql.install_as_MySQLdb()
import MySQLdb

from datetime import datetime

import telegram


# 텔레그램 토큰
telgm_token = '1635387024:AAEQfnk-F5A274EmpY1SSFY8bPYJbdULf2g'

# stoneheadcoding , @daegalibot, # 머리돌 채널 ID  : -1001280712219
bot = telegram.Bot(token = telgm_token)

stoneheadChannel = '-1001280712219'

# Initailize
# Db Connection (sqlalchemy ORM)
engine = create_engine('mysql://richman:richman@rasb:3306/richman', encoding='utf-8')

# Db Connection (pymysql)
conn = pymysql.connect(host='rasb', user='richman', password='richman', db='richman', charset='utf8', autocommit=True)

# Today (Ex:20210228)
today = datetime.today().strftime("%Y%m%d")
todayTime = datetime.today().strftime("%Y%m%d%H%M%S")

# Excel File Name
excelName = 'ETF_LIST_'+todayTime+'.xlsx'

# Excel 
writer = pd.ExcelWriter(excelName, engine='xlsxwriter')

# 텔레그램 봇 메세지 
def telgm_bot_send_msg(id, msg):
    bot.sendMessage(chat_id = id, text=msg)


def result_send_bot():
    today_etf_list()
    today_etf_result()

# 오늘 조회한 ETF 종목 조회 및 봇에게 보내기
def today_etf_list():
    try:
        # SQL문 실행
        sql = 'select rownum, itemname, changeRate from (select @rownum := @rownum + 1 as rownum, itemcode, itemname, nowVal, changeRate from etf_list A, (select @rownum := 0 ) TMP  where etfTabCode = 2 order by changeRate desc ) B where rownum between 1 and 20'
        curs = conn.cursor()
        curs.execute(sql)

        # 데이타 Fetch
        sqlResult = curs.fetchall()
        today = datetime.today().strftime("%Y-%m-%d %H:%M")
        result = '■■ Today :'+today +'■■\n\n'
        result += 'ETF 종목 등락률 1~20\n순위/이름/등락률\n\n'
        for data in sqlResult:
            result += str(int(data[0]))+'.\t'+data[1]+'\t'+str(data[2])+'\n'
        
        conn.close
        print(result)
        telgm_bot_send_msg(stoneheadChannel, result)
        # print(df)

    except Exception as e:
        print('today_etf_list error', +e)
        telgm_bot_send_msg(stoneheadChannel, 'today_etf_list 조회 실패' )
        
    finally:
        # return result
        print('today_etf_list finally')



# 오늘 조회한 ETF 종목, 가장 많은 종목 순서
def today_etf_result():
    try:
        # SQL문 실행
        sql = 'SELECT b.itemcode, b.itemname, COUNT(b.itemname) AS count FROM etf_result a, itemcode b WHERE 1=1 and a.itemcode = b.itemcode GROUP BY itemname HAVING COUNT(itemname) > 1 ORDER BY COUNT desc'
        curs = conn.cursor()
        curs.execute(sql)

        # 데이타 Fetch
        sqlResult = curs.fetchall()
        today = datetime.today().strftime("%Y-%m-%d %H:%M")

        result = '■■ Today :'+today +'■■\n\n'
        result += 'ETF 구성 종목 수\n종목코드/종목이름/개수\n\n'

        for data in sqlResult:
            result += str(data[0])+'.\t'+str(data[1])+'\t'+str(data[2])+'\n'
        
        conn.close
        print(result)
        telgm_bot_send_msg(stoneheadChannel, result)
        # print(df)

    except Exception as e:
        print('today_etf_list error', +e)
        telgm_bot_send_msg(stoneheadChannel, 'today_etf_list 조회 실패' )
        
    finally:
        # return result
        print('today_etf_list finally')


# 테이블 조회
def get_naver_etf_list():
    try:
        # Etf name get
        url = 'https://finance.naver.com/api/sise/etfItemList.nhn'  # 네이버 ETF 종목 리스트 API

        etfList_json = json.loads(requests.get(url).text)
        etfList_dataframe = json_normalize(etfList_json['result']['etfItemList'])
        etfList_dataframe = etfList_dataframe.sort_values(by='changeRate', ascending=False)

        time.sleep(3)
        # df = df[['itemcode','itemname']] # 특정 컬럼 선택

        # 인덱스 제거
        etfList_dataframe = etfList_dataframe.reset_index()
        print(etfList_dataframe)

        etfList_dataframe.to_excel(writer, sheet_name= 'ETF종목 리스트')
        etfList_dataframe.to_sql(name='etf_list', con=engine, if_exists='replace', index=False)

    except Exception:
        telgm_bot_send_msg(stoneheadChannel, 'ETF 코드 조회 실패(Naver API')
        print('get_naver_etf_list excute fail')

    finally:
        print('get_naver_etf_list excute success')
        return etfList_dataframe


# 테이블 조회
def get_etf_name(etf_list):
    try:
        
        result = pd.DataFrame()
        cnt = 0

        for index, row in etf_list.iterrows():
            if row['etfTabCode'] == 2 and cnt <= 20 :
                # print(row)
                time.sleep(2)
                cnt = cnt+1
                stockData = stock.get_etf_portfolio_deposit_file(row['itemcode'], today)
                stockData.insert(3, 'etfItemCode', row['itemcode'], False)
                stockData.insert(4, 'etfItemName', row['itemname'], False)

                stockData['티커'] = stockData.index
                stockData = stockData.reset_index(drop=True)
                stockData = stockData.rename(columns={'티커' : 'itemcode', '계약수' : 'amount', '금액' : 'price', '비중' : 'weight'}, index={'티커': '1'})

                if index == 0:
                    result = stockData
                else :
                    result = result.append(stockData)
                print(result)

        result.to_sql(name='etf_result', con=engine, if_exists='replace', index=True)
        result.to_excel(writer, sheet_name= 'ETF 구성 종목')

    except Exception:
        telgm_bot_send_msg(stoneheadChannel, '오늘의 종목 조회 실패')
        print('get_etf_name excute fail')
    finally:
        result_send_bot()
        print('get_etf_name excute success')
        

etf_list = get_naver_etf_list()
get_etf_name(etf_list)

writer.save()
conn.close()







        