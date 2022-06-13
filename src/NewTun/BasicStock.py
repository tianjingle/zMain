import sys

import tushare as ts
import pandas as pd
from sqlalchemy import create_engine

token= "f8b3f28da1e0f8eb79b7789b9ec7a6ceea9b8bfa68e5051bdff9c07d"
ts.set_token(token)

pro = ts.pro_api()
data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
df1 = pd.DataFrame(data)
df1=df1[~df1['ts_code'].str.contains("BJ")]###删除包含BJ字符的行
##将数据写入mysql的数据库，但需要先通过sqlalchemy.create_engine建立连接,且字符编码设置为utf8，否则有些latin字符不能处理
engine = create_engine('mysql+pymysql://root:tianjingle@localhost:3306/noun?charset=utf8')
df1.to_sql(name = 'stock_basic',con = engine,if_exists = 'append',index = False,index_label = False)