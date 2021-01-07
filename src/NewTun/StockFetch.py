from datetime import time

import pandas as pd
from sqlalchemy import create_engine
import baostock as bs


# 获取指定股票开始结束时间的股票数据
from src.NewTun.Connection import Connection


class StockFetch:

    # 获取股票数据
    def fetchByStartAndEndTime(self, code, startTime, endTime):
        if code == None:
            return
        if startTime == None:
            startTime = '1999-07-01'
        if endTime == None:
            endTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        lg = bs.login()
        rs = bs.query_history_k_data_plus(code,
                                          "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                          start_date=startTime, end_date=endTime,
                                          frequency="d", adjustflag="3")

        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        ##将数据写入mysql的数据库，但需要先通过sqlalchemy.create_engine建立连接,且字符编码设置为utf8，否则有些latin字符不能处理
        connection=Connection()
        connectionStr="mysql+pymysql://"+connection.user+":"+connection.passwd+"@"+connection.host+":"+str(connection.port)+"/"+connection.db+"?charset=utf8"
        engine = create_engine(connectionStr)
        # 插入数据库
        result.to_sql(name=code, con=engine, if_exists='append', index=False, index_label=False)
