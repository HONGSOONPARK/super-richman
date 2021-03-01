# from pykrx import stock
# df = stock.get_etf_portfolio_deposit_file("305720", "20210216")
# print(df)
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

# db 연결
engine = create_engine('mysql://richman:richman@rasb:3306/richman', encoding='utf-8')
conn = engine.connect()
time.sleep(3)

df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]

df['종목코드'] = df['종목코드'].map(lambda x: f'{x:0>6}')
df = df[['종목코드', '회사명']]
df = df.rename(columns={'회사명': 'itemname', '종목코드': 'itemcode'})

df.to_sql(name='itemcode', con=engine, if_exists='replace', index=False)
conn.close()