import sys

import tushare as ts
import pandas as pd
from sqlalchemy import create_engine


pro = ts.pro_api()
data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
result = pd.DataFrame(data)
##将数据写入mysql的数据库，但需要先通过sqlalchemy.create_engine建立连接,且字符编码设置为utf8，否则有些latin字符不能处理
engine = create_engine('mysql+pymysql://root:tianjingle@localhost:3307/noun?charset=utf8')
result.to_sql(name = 'stock_basic',con = engine,if_exists = 'append',index = False,index_label = False)