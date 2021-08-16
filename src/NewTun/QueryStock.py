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

        maxPrice=talib.MAX(result['close'],data)[len(result)-1]
        print(maxPrice)
        result.date = range(0, len(result))  # 日期改变成序号
        resultTemp.append(result)
        resultTemp.append(maxPrice)
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