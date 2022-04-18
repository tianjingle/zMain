import datetime
import time
import threadpool

import pymysql.cursors
from src.NewTun.Connection import Connection
from src.NewTun.JgdyQuery import JgdyQuery
from src.NewTun.StockFetch import StockFetch
from src.NewTun.TDX.Core import Core


class StockInfoSyn:

    #是否拉取机构调研消息
    isJgdy=False

    stockMap={}

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

    def doSyn(self,i,stockTemp,endTime):
        # 获取游标
        connection = Connection()
        connect = pymysql.Connect(
            host=connection.host,
            port=connection.port,
            user=connection.user,
            passwd=connection.passwd,
            db=connection.db,
            charset=connection.charset
        )
        cursor = connect.cursor()
        startTime = ''

        for row in stockTemp:
            isToady = False
            print("thread-" + str(i) +" - " + row)
            realCode = self.tuShareCode2BaoStockCode(row)
            tableCheckSql = "show tables like '" + realCode + "'"
            cursor.execute(tableCheckSql)
            if len(list(cursor)) == 0:
                print("no data of " + realCode)
                startTime = '2015-01-01'
            else:
                # 查找股票的最近时间
                sql = "SELECT * FROM `%s` order by date desc limit 1;"
                data = (realCode)
                cursor.execute(sql % data)
                # 如果没有数据那么设置为1997年开始
                for row in cursor.fetchall():
                    startTime1 = row[0]
                    if startTime1 == endTime:
                        isToady = True
                        continue
                    str_p = startTime1 + ' 0:29:08'
                    dateTime_p = datetime.datetime.strptime(str_p, '%Y-%m-%d %H:%M:%S')
                    startTime = (dateTime_p + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
            if isToady == True:
                print(realCode + "--不需要同步了。。")
            else:
                print("syn  " + realCode)
                fectExecute = StockFetch()
                # 优先从通达信获取数据
                if connection.tdxDayPath == '':
                    fectExecute.fetchByStartAndEndTime(realCode, startTime, endTime)
                else:
                    fectExecute.parseDataFromCvs(connection.tdxDayPath, realCode, startTime, endTime)
            if self.isJgdy == 'True':
                jgdy = JgdyQuery()
                jgdy.printJgdyInfo(realCode.split('.')[1], 1)


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
        endTime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        stockCodeList=[]

        stockCodeList.append("sh.000001")
        for row in cursor.fetchall():
            stockCodeList.append(row[0])
        self.doSyn(1,stockCodeList,endTime)
        print("--------------syn---------end....")
        cursor.close()
        connect.close()


