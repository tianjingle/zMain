import datetime
import time

import pymysql.cursors
from src.NewTun.Connection import Connection
from src.NewTun.StockFetch import StockFetch


class StockInfoSyn:

    #tushare code转化为baostock code
    def tuShareCode2BaoStockCode(self,tuShareCode):
        code=tuShareCode.lower().split('.')
        realCode=code[1]+"."+code[0]
        return realCode

    #baostock code转tushare code
    def BaoStockCode2tuShareCode(self,BaoCode):
        code=BaoCode.upper().split('.')
        realCode=code[1]+"."+code[0]
        return realCode


    #获取基本股票
    def getBiscicStock(self):
        stockList=[]
        connection=Connection()
        connect = pymysql.Connect(
            host=connection.host,
            port=connection.port,
            user=connection.user,
            passwd=connection.passwd,
            db=connection.db,
            charset=connection.charset
        )
        cursor = connect.cursor()
        allStockBasic = "select * from stock_basic"
        # allStockBasic = "select * from stock_basic where ts_code='300377.sz'"
        cursor.execute(allStockBasic)
        for row in cursor.fetchall():
            realCode = self.tuShareCode2BaoStockCode(row[0])
            temp=[]
            temp.append(realCode)
            temp.append(row[2])
            temp.append(row[3])
            temp.append(row[4])
            stockList.append(temp)
        cursor.close()
        connect.close()
        return stockList

    def synStockInfo(self):
        # 获取游标
        connection=Connection()
        connect = pymysql.Connect(
            host=connection.host,
            port=connection.port,
            user=connection.user,
            passwd=connection.passwd,
            db=connection.db,
            charset=connection.charset
        )
        cursor = connect.cursor()
        allStockBasic='select * from stock_basic'
        cursor.execute(allStockBasic)
        startTime=''
        endTime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        for row in cursor.fetchall():
            print(row[0])
            realCode=self.tuShareCode2BaoStockCode(row[0])
            tableCheckSql = "show tables like '"+realCode+"'"
            cursor.execute(tableCheckSql)
            if len(list(cursor))==0:
                print("no data of "+realCode)
                startTime='1997-07-01'
            else:
                # 查找股票的最近时间
                sql = "SELECT * FROM `%s` order by date desc limit 1;"
                data = (realCode)
                cursor.execute(sql % data)
                #如果没有数据那么设置为1997年开始
                for row in cursor.fetchall():
                    startTime1=row[0]
                    if startTime1==endTime:
                        continue
                    str_p = startTime1+' 0:29:08'
                    dateTime_p = datetime.datetime.strptime(str_p, '%Y-%m-%d %H:%M:%S')
                    startTime=(dateTime_p + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
            if startTime==endTime:
                print(realCode+"--不需要同步了。。")
            else:
                print("syn  "+realCode)
                fectExecute= StockFetch()
                fectExecute.fetchByStartAndEndTime(realCode,startTime,endTime)
        cursor.close()
        connect.close()
