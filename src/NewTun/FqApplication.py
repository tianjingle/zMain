import os
import time

import pymysql

from src.NewTun.Connection import Connection
from src.NewTun.Fq import Fq


class FqApplication:

    #复权检测
    fq=Fq()
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
    # fuquan="C:\\Users\\Administrator\\PycharmProjects\\zMain\\src\\NewTun\\fuquan"
    fuquan=os.path.join(os.path.dirname(__file__), "fuquan")
    map={}
    netMap={}
    count=0
    codeMap = {}

    def __init__(self):
        print("-------复权------")
        cursor = self.connect.cursor()
        allStockBasic = 'select * from stock_basic'
        cursor.execute(allStockBasic)
        for row in cursor.fetchall():
            code = row[0].upper()
            code = code.replace("SH", "").replace("SZ", "").replace(".", "")
            self.codeMap[code]=row[0]
        #转化为map
        self.toMap()
        self.netMap=self.fq.fhpf()




    #警句整理，去除序号和开都的标点符号
    def toMap(self):
        fo = open(self.fuquan,"r",encoding='gbk')
        for line in fo.readlines():
            key=line.replace("\n","")
            self.map[key]="1"
        fo.flush()
        fo.close()


    #从文件中获取一个警句
    def map2File(self):
        list = []
        for key in self.map:
            list.append(key+"\n")
        f = open(self.fuquan, "w", encoding='gbk')
        f.writelines(list)
        f.flush()
        f.close()


    #删除表
    def dropTable(self,code):
        print(code)
        #排除特殊的版本，比如8888开头的
        if self.codeMap.__contains__(code):
            code=self.codeMap[code]
            code=code.lower()
            codes=code.split('.')
            realCode=codes[1]+"."+codes[0]
            tableCheckSql = "show tables like '" + realCode + "'"
            cursor = self.connect.cursor()
            cursor.execute(tableCheckSql)
            if len(list(cursor)) == 0:
                print("no data of table" + realCode)
                return
            sql="drop table `"+realCode+"`"
            print(sql)
            cursor = self.connect.cursor()
            cursor.execute(sql)

    def start(self):
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        for key in self.netMap:
            if self.map.__contains__(key)==False:
                day=key.split("_")[1]
                if day == today:
                    # 新的需要删除的表加入缓存
                    self.map[key] = "1"
                    # 删除表
                    self.dropTable(key.split("_")[0])
        #存入数据库
        self.map2File()


#复权删除，并重新拉数据
# FQ=FqApplication()
# FQ.start()
