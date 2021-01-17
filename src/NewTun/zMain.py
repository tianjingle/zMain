import time
import os
import uuid
import pymysql

from src.NewTun.ApplicationWithDraw import ApplicationWithDraw
from src.NewTun.Connection import Connection
from src.NewTun.JgdyQuery import JgdyQuery
from src.NewTun.QueryStock import QueryStock
from src.NewTun.SendEmail import SendEmail
from src.NewTun.Statistics import Statistics
from src.NewTun.StockInfoSyn import StockInfoSyn
from src.NewTun.Application import Application


class zMain:

    #是否显示出来
    isShow=True
    candidate=[]
    currentPath=''
    connection = None
    def __init__(self):
        self.currentPath=os.getcwd()
        self.connection = Connection()


    #通过股票数据
    def synHistoryStock(self):
        if self.connection.syn=='True':
            print("-----------------------------syn stock------------------------------------")
            print("start time:"+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            syn=StockInfoSyn()
            syn.synStockInfo()
            print("start time:"+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


    # #扫描潜在可以投资的股票
    def scanStock(self):
        query = QueryStock()
        today=query.todayIsTrue()[0]
        connect = pymysql.Connect(
            host=self.connection.host,
            port=self.connection.port,
            user=self.connection.user,
            passwd=self.connection.passwd,
            db=self.connection.db,
            charset=self.connection.charset
        )
        # 获取游标
        cursor = connect.cursor()
        tableCheckSql = "show tables like 'candidate_stock'"
        cursor.execute(tableCheckSql)
        if len(list(cursor)) == 0:
            createTable = "create table candidate_stock(id varchar(64) primary key not null,code varchar(64),name varchar(64),collect_date varchar(64),industry varchar(64),grad float,cv float,price float,now_price float,profit float,other varchar(45),is_down_line int)"
            cursor.execute(createTable)
        print("-----------------------------scan stock------------------------------------")
        print("start time:" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        syn = StockInfoSyn()
        basicStock = syn.getBiscicStock()
        count = 0
        for item in basicStock:
            count = count + 1
            test = Application()
            print(str(count) + "     " + item[0]+"     "+item[1]+"    "+item[2]+"    "+item[3])
            kk = test.execute(item[0])
            if test.avgCostGrad < 0:
                candidateTemp = []
                candidateTemp.append(item[0])
                candidateTemp.append(item[1])
                candidateTemp.append(item[3])
                candidateTemp.append(test.avgCostGrad)
                self.candidate.append(candidateTemp)
                # 插入数据
                sql = "select * from candidate_stock where code='%s' and collect_date='%s'"
                data = (item[0], today)
                cursor.execute(sql % data)
                if len(list(cursor)) == 0:
                    print(item)
                    sql = "INSERT INTO candidate_stock (id, code, name,collect_date,industry,grad,cv,is_down_line) VALUES ( '%s', '%s','%s', '%s','%s', %.8f, %.8f,%i)"
                    data = (uuid.uuid1(), item[0], item[1],today,item[3],test.avgCostGrad,test.cvValue,test.isDownLine)
                    cursor.execute(sql % data)
                connect.commit()
            # 垃圾回收
            del kk, test
            if count == int(self.connection.scans):
                print("测试退出")
                break

    #按照程度的梯度排序
    def sortByStockGrad(self):
        self.candidate=sorted(self.candidate, key=lambda s: s[3])


    #展示筛选的股票
    def stockShow(self):
        for item in self.candidate:
            test = ApplicationWithDraw()
            test.execute(item[0],True,self.currentPath)
            print(str(item[1])+"   "+item[0]+"   "+str(item[3]))



zm=zMain()
sendEmail=SendEmail()
s=Statistics()
#同步历史数据
zm.synHistoryStock()
# #扫描选股
# zm.scanStock()
# #股票排名
zm.sortByStockGrad()
# #作图
zm.stockShow()
#统计股票盈利情况
s.fetchStocks()
# 分类股票推荐发送
sendEmail.sendYouCanBuy(zm.currentPath)


