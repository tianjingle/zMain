import json
import sys
from datetime import time
import time

import pandas as pd
import pymysql
from sqlalchemy import create_engine
import baostock as bs


# 获取指定股票开始结束时间的股票数据
from src.NewTun.Connection import Connection
from src.NewTun.ReadTdx2Db import ReadTdx2Db
from src.NewTun.RunTimeExecute import RunTimeExecute
from src.NewTun.Tencent import Tencent


class StockFetch:

    tdxData=None
    first=True
    tencent=None
    connection = Connection()
    connectionStr = "mysql+pymysql://" + connection.user + ":" + connection.passwd + "@" + connection.host + ":" + str(
        connection.port) + "/" + connection.db + "?charset=utf8"
    engine = create_engine(connectionStr, pool_size=20, pool_recycle=60)

    def __init__(self):
        self.tdxData=ReadTdx2Db()
        self.tencent=Tencent()

    # 获取股票数据
    def fetchByStartAndEndTime(self, code, startTime, endTime):
        if code == None:
            return
        if startTime == None:
            startTime = '2015-07-01'
        if endTime == None:
            endTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        lg = bs.login()
        rs = bs.query_history_k_data_plus(code,
                                          "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                          start_date=startTime, end_date=endTime,
                                          frequency="d", adjustflag="2")

        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        if code=='sh.000001':
            if len(result) == 0:
                print("no data from baostock,maybe it is holiday!")
                sys.exit()
            return

        ##将数据写入mysql的数据库，但需要先通过sqlalchemy.create_engine建立连接,且字符编码设置为utf8，否则有些latin字符不能处理
        connection=Connection()
        connectionStr="mysql+pymysql://"+connection.user+":"+connection.passwd+"@"+connection.host+":"+str(connection.port)+"/"+connection.db+"?charset=utf8"
        engine = create_engine(connectionStr,pool_size=20, pool_recycle=60)
        # 插入数据库
        result.to_sql(name=code, con=engine, if_exists='append', index=False, index_label=False)



    def fetchDataFromEasyquotation2Cache(self,code,endDate):
        now = self.tencent.getCurrentStockInfo(code)
        tradestatus=1
        isSt=0
        #时间对应上，则拉数据
        if str(now['datetime']).split(" ")[0]!=endDate:
            print("非本日数据...无法拉取")
            return
        if now['open']==0 and now['volume']==0:
            tradestatus=0
        if now['name'].__contains__("ST"):
            isSt=1

        mark=RunTimeExecute()
        hour=time.localtime().tm_hour
        if int(hour) < 15 and int(hour)>=9:
            #当日15点之前跑的数据，统一写到cache中，不写数据库
            tianjl={'date': endDate,
                 'code':code,
                 'open': now['open'],
                 'high': now['high'],
                 'low': now['low'],
                 'close': now['now'],
                 'volume': now['volume'],
                 'tradestatus':tradestatus,
                 'turn': now['turnover'],
                 'isST':isSt}
            mark.writeRunTime2Cache(endDate+"_"+code+"_"+str(json.dumps(tianjl)))

    # 获取数据
    def fetchDataFromEasyquotation(self,code,endDate):
        # result = pd.DataFrame({'source': ["date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST"]})
        result = pd.DataFrame()
        now = self.tencent.getCurrentStockInfo(code)
        tradestatus=1
        isSt=0
        #时间对应上，则拉数据
        if str(now['datetime']).split(" ")[0]!=endDate:
            print("非本日数据...无法拉取")
            return
        if now['open']==0 and now['volume']==0:
            tradestatus=0
        if now['name'].__contains__("ST"):
            isSt=1
        # "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST"

        tian = [{'date': endDate,
                 'code':code,
                 'open': now['open'],
                 'high': now['high'],
                 'low': now['low'],
                 'close': now['now'],
                 'volume': now['volume'],
                 'tradestatus':tradestatus,
                 'turn': now['turnover'],
                 'isST':isSt}]

        mark=RunTimeExecute()
        ymd,hour=mark.fetchMarkRunTime()
        if ymd==endDate and int(hour) < 15 and int(hour)>=9:
            #当日15点之前跑的数据，统一写到cache中，不写数据库
            tianjl={'date': endDate,
                 'code':code,
                 'open': now['open'],
                 'high': now['high'],
                 'low': now['low'],
                 'close': now['now'],
                 'volume': now['volume'],
                 'tradestatus':tradestatus,
                 'turn': now['turnover'],
                 'isST':isSt}
            mark.writeRunTime2Cache(endDate+"_"+code+"_"+str(json.dumps(tianjl)))
        else:
            #15点之后写到数据库中
            result = result.append(tian, ignore_index=True)
            # 插入数据库
            result.to_sql(name=code, con=self.engine, if_exists='append', index=False, index_label=False)




    def parseDataFromCvs(self,path,code, startTime, endTime):
        file=code.split(".")[1]
        temp=self.tdxData.readData(path+file+".csv",startTime,endTime)
        sql="insert into noun.`"+code+"` values"
        if len(temp)<=0:
            return
        sqlTemp=""
        # '2021-07-15', '000002', '23.21', '23.73', '23.01', '23.52', '63981243', '1498254976'
        for item in temp:
            sqlTemp=sqlTemp+",('"+item[0]+"','"+code+"','"+item[2]+"','"+item[3]+"','"+item[4]+"','"+item[5]+"',"+"0,'"+item[6]+"','"+item[7]+"',2,'"+item[11]+"',1,0,0)"
        sqlTemp=sqlTemp.strip(",")
        sql=sql+sqlTemp
        connection = Connection()
        connect = pymysql.Connect(
            host=connection.host,
            port=connection.port,
            user=connection.user,
            passwd=connection.passwd,
            db=connection.db,
            charset=connection.charset
        )
        # 获取游标
        cursor = connect.cursor()
        cursor.execute(sql)
        connect.commit()


# StockFetch().fetchDataFromEasyquotation("sh.600090",'2022-05-19')






