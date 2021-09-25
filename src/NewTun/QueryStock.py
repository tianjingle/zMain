import datetime
import time

import numpy as np
import talib
import pymysql.cursors
import pandas as pd
from src.NewTun.Connection import Connection
from src.NewTun.ZSIndex import ZSIndex


class QueryStock:

    window=200
    code=''
    start=0
    isIndex=False

    def init(self,window):
        self.window=window+80

    def queryStock(self, stackCode):
        # 连接数据库
        resultTemp=[]
        connection=Connection()
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
        # 查询数据
        sql = "select * from (SELECT DISTINCT * FROM `"+stackCode+"` where tradestatus=1 and turn is not null order by date desc limit %i) as b order by date asc"
        data = (self.window+80)
        cursor.execute(sql % data)
        fs = cursor.description
        filelds = []
        for field in fs:
            filelds.append(field[0])
        rs = cursor.fetchall()
        result = pd.DataFrame(list(rs), columns=filelds)
        # 关闭连接
        cursor.close()
        connect.close()
        #二维数组
        result=result.loc[:,['date','open','high','low','close','volume','turn','tradestatus'] ]

        #计算三十日均线
        result['M30']=talib.SMA(result['close'],30)
        result['T30']=talib.T3(result['close'],timeperiod=30, vfactor=0)
        result['tprice']=talib.TYPPRICE(result['high'],result['low'],result['close'])
        # slowk, slowd = talib.STOCH(result['high'],result['low'],result['close'], fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        # slowj= list(map(lambda x,y: 3*x-2*y, slowk, slowd))
        # result['k']=slowk
        # result['d']=slowd
        # result['j']=slowj
        zsindex=ZSIndex()
        # 主力线，散户线
        zz, ss = zsindex.zsLine(result)
        mm = zsindex.convertXQH(result)
        result['z'] = zz
        result['s'] = ss
        result['m'] = mm
        #神仙趋势线
        result['h1']=talib.EMA(result['close'],6)
        result['h2']=talib.EMA(result['h1'],18)
        result['h3']=talib.EMA(result['close'],108)

        result['VAR618']=618
        result['VAR100']=100
        result['VAR10']=10
        result['VAR0']=0

        #主力散户吸筹
        # VAR2:=REF(LOW,1);      前一日的最低价
        result['VAR2'] = result['low']
        result['VAR2']=result['VAR2'].shift(1)
        result=result.fillna(0)
        result['low']=result['low'].astype(float)
        result['VAR2']=result['VAR2'].astype(float)
        result['closeP']=result['close']
        result['closeP']=result['closeP'].astype(float)

        # VAR3 := SMA(ABS(LOW - VAR2), 3, 1) / SMA(MAX(LOW - VAR2, 0), 3, 1) * 100;
        result['LOW_VAR2']=result['low']-result['VAR2']
        result['var3Pre']=talib.SMA(result['LOW_VAR2'].abs(),3)
        result = result.assign(var3sub=np.where(result.LOW_VAR2 > 0, result.LOW_VAR2, 0.00000000000000000001))
        result['var3sub']=talib.SMA(result['var3sub'],3)

        result['VAR3']=talib.MULT(talib.DIV(result['var3Pre'],result['var3sub']),result['VAR100'])
        result=result.assign(tianjingle=np.where(result.closeP*1.3!=0,round(result.VAR3*10,2),result.VAR3/10))
        result['tianjingle']=result['tianjingle'].astype(float)
        result['tianjingle'].fillna(0)
        result['VAR4']=talib.EMA(result['tianjingle'],3)
        #print(result['VAR4'])
        # VAR5 := LLV(LOW, 30);
        result['VAR5']=result['low'].rolling(30).min()
        # VAR6 := HHV(VAR4, 30);
        result['VAR6']=result['VAR4'].rolling(30).max()
        #print(result['VAR6'])
        # VAR7 := IF(MA(CLOSE, 58), 1, 0);
        result['VAR7temp']=talib.MA(result['close'], 58)
        #这里做判断
        result=result.assign(VAR7=np.where(result.VAR7temp!=0,1,0))
        # VAR8 := EMA(IF(LOW <= VAR5, (VAR4 + VAR6 * 2) / 2, 0), 3) / 618 * VAR7;
        result=result.assign(VAR8TEMP=np.where(result.low<=result.VAR5,(result.VAR4+result.VAR6*2)/2,0))
        result['VAR8TEMP']=talib.EMA(result['VAR8TEMP'],3)
        result['VAR8']=talib.MULT(talib.DIV(result['VAR8TEMP'],result['VAR618']),result['VAR7'])
        #print(result['VAR8'].max())
        #print(result['VAR8'].min())
        result['VAR8']=result['VAR8']/10000000000000000000
        # VAR9 := IF(VAR8 > 100, 100, VAR8);
        result=result.assign(VAR9=np.where(result.VAR8>100,100,result.VAR8))
        #输出吸筹:当满足条件VAR9>-120时,在0和VAR9位置之间画柱状线,宽度为2,5不为0则画空心柱.,画洋红色
        # 输出地量:当满足条件0.9上穿1/成交量(手)*1000>0.01AND"KDJ的J"<0时,在最低价*1位置书写文字,COLOR00FFFF
        # 吸筹: STICKLINE(VAR9 > -120, 0, VAR9, 2, 5), COLORMAGENTA;
        # 地量: DRAWTEXT(CROSS(0.9, 1 / VOL * 1000 > 0.01 AND "KDJ.J" < 0), L * 1, '地量'), COLOR00FFFF;
        result=result.assign(VARXC=np.where(result.VAR9>30,result.VAR9,0))
        t=result['VARXC'][-1:].iloc[0]
        # print("最后的一个"+str(t))
        #print(result[['low','VAR4','VAR5','VAR6','VAR7','VAR8','VAR9','VARXC']])

        maxPrice=talib.MAX(result['close'],data)[len(result)-1]
        self.start=len(result)-self.window
        # print(maxPrice)
        result.date = range(0, len(result))  # 日期改变成序号
        resultTemp.append(result)
        resultTemp.append(maxPrice)
        resultTemp.append(t)
        return resultTemp

    def queryYouCanBuyStock(self):
        # 连接数据库
        codes=[]
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
        # 获取游标
        today = self.todayIsTrue()[0]
        # 查询数据
        sql = "SELECT * FROM `candidate_stock` where collect_date='%s' order by cv asc,grad desc"
        data = (today)
        cursor.execute(sql % data)
        for row in cursor.fetchall():
            temp=[]
            temp.append(row[1])
            temp.append(row[2])
            temp.append(row[3])
            temp.append(row[4])
            temp.append(row[5])
            #主力、散户、反转
            temp.append(row[12])
            temp.append(0)
            codes.append(temp)
        # 关闭连接
        cursor.close()
        connect.close()
        return codes


    def todayKlineByCode(self,code):
        # 连接数据库
        price=0
        connection=Connection()
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
        # 查询数据
        sql = "SELECT * FROM `"+code+"` where tradestatus=1 and turn is not null order by date desc limit 1"
        cursor.execute(sql)
        for row in cursor.fetchall():
            price=float(row[5])
        # 关闭连接
        cursor.close()
        connect.close()
        return price

    #获取你可能购买的股票历史数据
    def queryHistoryStock(self):
        codeList=[]
        sql='SELECT * FROM candidate_stock'
        # 连接数据库
        connection=Connection()
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
        # 查询数据
        cursor.execute(sql)
        for row in cursor.fetchall():
            temp=[]
            temp.append(row[0])
            temp.append(row[1])
            temp.append(row[2])
            temp.append(row[3])
            temp.append(row[4])
            temp.append(row[5])
            codeList.append(temp)
        # 关闭连接
        cursor.close()
        connect.close()
        return codeList

    #获取两天的价格
    def fetchPriceList(self, code,collectTime):
        prices = []
        sql = "SELECT close,date FROM `"+code+"` where date ='"+collectTime+"' union all (select close,date from  `"+code+"` order by date desc limit 1)"
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
        # 查询数据
        cursor.execute(sql)
        for row in cursor.fetchall():
            temp=[]
            temp.append(row[0])
            temp.append(row[1])
            prices.append(temp)
        if len(prices)==1:
            prices.append(prices[0])
        # 关闭连接
        cursor.close()
        connect.close()
        return prices

    #更新候选股票的价格
    def updateCandidate(self, id, oldPrice, nowPrice, profit,time):
        sql = "update  candidate_stock set other='"+time+"', price= " + str(oldPrice) + ",now_price="+str(nowPrice)+",profit="+str(profit)+" where id ='" + id + "'"
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
        # 查询数据
        cursor.execute(sql)
        connect.commit()
        # 关闭连接
        cursor.close()
        connect.close()

    #获取最经的交易日期
    def todayIsTrue(self):
        temp = []
        sql = "SELECT max(date) FROM `sh.600000`"
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
        # 查询数据
        cursor.execute(sql)
        for row in cursor.fetchall():
            temp.append(row[0])
        # 关闭连接
        cursor.close()
        connect.close()
        return temp

    def queryStockYouBrought(self,statisticSql):
        result=[]

        sql = "select a.* from candidate_stock a inner join (SELECT id,code,min(collect_date),profit from candidate_stock where "+statisticSql+" group by code order by profit desc) b where a.id=b.id"
        connection = Connection()
        connect = pymysql.Connect(
            host=connection.host,
            port=connection.port,
            user=connection.user,
            passwd=connection.passwd,
            db=connection.db,
            charset=connection.charset,
            sql_mode="STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION"
        )
        # 获取游标
        cursor = connect.cursor()
        # 查询数据
        cursor.execute(sql)
        for row in cursor.fetchall():
            temp=[]
            temp.append(row[1])
            temp.append(row[2])
            temp.append(row[3])
            temp.append(row[5])
            temp.append(row[6])
            temp.append(row[7])
            temp.append(row[8])
            temp.append(row[9])
            # temp.append(row[10])
            result.append(temp)
        # 关闭连接
        cursor.close()
        connect.close()
        return result


    def queryStockForTestJgdy(self,sql):
        result=[]
        connection = Connection()
        connect = pymysql.Connect(
            host=connection.host,
            port=connection.port,
            user=connection.user,
            passwd=connection.passwd,
            db=connection.db,
            charset=connection.charset,
            sql_mode="STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION"
        )
        # 获取游标
        cursor = connect.cursor()
        # 查询数据
        cursor.execute(sql)
        for row in cursor.fetchall():
            temp=[]
            temp.append(row[1])
            temp.append(row[2])
            temp.append(row[3])
            temp.append(row[5])
            temp.append(row[6])
            temp.append(row[7])
            temp.append(row[8])
            temp.append(row[9])
            temp.append(row[10])
            result.append(temp)
        # 关闭连接
        cursor.close()
        connect.close()
        return result

    def queryStock20DayReccently(self):
        # 连接数据库
        codes=[]
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
        # 获取游标
        str_p = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        dateTime_p = datetime.datetime.strptime(str_p, '%Y-%m-%d %H:%M:%S')
        startTime = (dateTime_p + datetime.timedelta(days=-20)).strftime("%Y-%m-%d")
        # 查询数据
        sql = "SELECT distinct * FROM `candidate_stock` where zsm=2 and collect_date>'%s' order by cv asc,grad desc"
        data = (startTime)
        cursor.execute(sql % data)
        for row in cursor.fetchall():
            temp=[]
            temp.append(row[1])
            temp.append(row[2])
            temp.append(row[3])
            temp.append(row[4])
            temp.append(row[5])
            #主力、散户、反转
            temp.append(row[12])
            codes.append(temp)
        # 关闭连接
        cursor.close()
        connect.close()
        return codes

    def queryStockBC(self):
        str_p = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        dateTime_p = datetime.datetime.strptime(str_p, '%Y-%m-%d %H:%M:%S')
        startTime = (dateTime_p + datetime.timedelta(days=-20)).strftime("%Y-%m-%d")

        # 连接数据库
        codes = []
        connection = Connection()
        connect = pymysql.Connect(
            host=connection.host,
            port=connection.port,
            user=connection.user,
            passwd=connection.passwd,
            db=connection.db,
            charset=connection.charset,
            sql_mode="STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION"
        )
        cursor = connect.cursor()
        # 查询数据
        sql = "select a.* from candidate_stock a inner join (SELECT id,code,min(collect_date),profit from candidate_stock where  collect_date>'%s' and dl=1 group by code order by profit desc) b where a.id=b.id"
        data = (startTime)
        cursor.execute(sql % data)
        for row in cursor.fetchall():
            temp = []
            temp.append(row[1])
            temp.append(row[2])
            temp.append(row[3])
            temp.append(row[4])
            temp.append(row[5])
            # 主力、散户、反转
            temp.append(row[12])
            temp.append(1)
            codes.append(temp)
        # 关闭连接
        cursor.close()
        connect.close()
        return codes